import {useCallback, useRef, useState} from 'react';
import axios from 'axios';
import './App.css';

enum Status {
  TRANSFERRING = 'TRANSFERRING',
  PROCESSING = 'PROCESSING',
  INGESTING = 'INGESTING',
  CLEANING_UP = 'CLEANING_UP',
  SUCCESS = 'SUCCESS',
}

const MESSAGES: Record<Status, string> = {
  [Status.TRANSFERRING]: 'Preparing your files',
  [Status.PROCESSING]: 'Crunching the math',
  [Status.INGESTING]: 'Indexing data for visualization. Go outside, this will take a while.',
  [Status.CLEANING_UP]: 'Cleaning up',
  [Status.SUCCESS]: 'All done',
} as const;

// if i expect more than a few concurrent jobs across clients
// i'll definitely have to move this to websockets
const POLL_INTERVAL = 20;

function App() {
  const inputRef = useRef<HTMLInputElement>(null);
  const [dataStatus, setDataStatus] = useState<Status | null>(null);
  const [progress, setProgress] = useState(0);

  const onFile = useCallback(async () => {
    if (!inputRef?.current) {
      return;
    }
    const files = inputRef.current.files ?? [];
    setDataStatus(Status.TRANSFERRING);
    const {data: jobMetadata} = await axios.postForm('http://localhost:3005/upload', {
      'files[]': files,
    });

    let status = Status.TRANSFERRING;
    let totalRows = 0;
    setDataStatus(status);
    while (status !== 'SUCCESS') {
      await new Promise(resolve => setTimeout(resolve, POLL_INTERVAL));
      const {data} = await axios.get(`http://localhost:3005/job/${jobMetadata.jobId}`);
      status = data.status as Status
      totalRows = data.total_rows;
      setProgress(data.rows_ingested / totalRows)
      setDataStatus(status);
    }
  }, []);

  return (
    <div className='upload-pipeline'>
      <input
        type='file'
        id='file'
        name='file'
        multiple
        accept='.csv'
        onChange={onFile}
        ref={inputRef}
      />
      {dataStatus !== null && (
        <p>{MESSAGES[dataStatus]}</p>
      )}
      {dataStatus === Status.INGESTING && (
        <p>{(progress * 100).toFixed(2)}%</p>
      )}
      <br />
      <iframe
        src="http://localhost:3000/d-solo/buoy/new-dashboard?orgId=1&from=1609488000000&to=1641024000000&timezone=browser&panelId=1&__feature.dashboardSceneSolo"
        width="500"
        height="500"
        frameBorder="0"
      />
      <iframe
        src="http://localhost:3000/d-solo/buoy/new-dashboard?orgId=1&from=1609488000000&to=1641024000000&timezone=browser&refresh=10s&panelId=2&__feature.dashboardSceneSolo"
        width="500"
        height="500"
        frameBorder="0"
      />
    </div>
  )
}

export default App
