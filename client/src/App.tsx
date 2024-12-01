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
  const [uploadStatus, setUploadStatus] = useState<Status | null>(null);
  const [rowsProcessed, setRowsProcessed] = useState(0);
  const [progress, setProgress] = useState(0);

  const onFile = useCallback(async () => {
    if (!inputRef?.current) {
      return;
    }
    const files = inputRef.current.files ?? [];
    setUploadStatus(Status.TRANSFERRING);
    const {data: jobMetadata} = await axios.postForm('http://localhost:3005/upload', {
      'files[]': files,
    });

    let status = Status.TRANSFERRING;
    let totalRows = 0;
    setUploadStatus(status);
    while (status !== 'SUCCESS') {
      await new Promise(resolve => setTimeout(resolve, POLL_INTERVAL));
      const {data} = await axios.get(`http://localhost:3005/job/${jobMetadata.jobId}`);
      status = data.status as Status
      totalRows = data.total_rows;
      setRowsProcessed(data.rows_ingested);
      setProgress(data.rows_ingested / totalRows)
      setUploadStatus(status);
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
      {uploadStatus !== null && (
        <p>{MESSAGES[uploadStatus]}</p>
      )}
      {uploadStatus === Status.INGESTING && (
        <>
          <p>{`Indexed rows: ${rowsProcessed}`}</p>
          <p>{(progress * 100).toFixed(2)}%</p>
        </>
      )}
    </div>
  )
}

export default App
