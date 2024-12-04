import {useCallback, useRef, useState} from 'react';
import axios from 'axios';
import {delay} from './utils';

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
  [Status.INGESTING]: 'Indexing data for visualization',
  [Status.CLEANING_UP]: 'Cleaning up',
  [Status.SUCCESS]: 'All done',
} as const;

// if i expect more than a few concurrent jobs across clients
// i'll definitely have to move this to websockets
const POLL_INTERVAL = 20;

export default function Upload() {
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
      await delay(POLL_INTERVAL);
      const {data} = await axios.get(`http://localhost:3005/job/${jobMetadata.jobId}`);
      status = data.status as Status
      totalRows = data.total_rows;
      setProgress(data.rows_ingested / totalRows * 100);
      setDataStatus(status);
    }
  }, []);

  return (
    <div className='upload'>
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
        <p className='upload-message'>{MESSAGES[dataStatus]}</p>
      )}
      {dataStatus === Status.INGESTING && (
        <progress id="file" max="100" value={progress.toFixed(2)} />
      )}
    </div>
  )
}
