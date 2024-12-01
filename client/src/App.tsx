import {useCallback, useRef, useState} from 'react';
import axios, {AxiosProgressEvent} from 'axios';
import './App.css';

const MESSAGES = {
  TRANSFERRING: 'Preparing your files',
  PROCESSING: 'Crunching the math',
  INGESTING_DISPLACEMENT: 'Storing displacement results',
  INGESTING_LOCATION: 'Storing location results',
  CLEANING_UP: 'Cleaning up',
  SUCCESS: 'All done',
} as const;

const TIMEOUT = 1000 * 60 * 5 // 5 mins
const POLL_INTERVAL = 1000;

function App() {
  const inputRef = useRef<HTMLInputElement>(null);
  const [uploadStatus, setUploadStatus] = useState('');
  const [rowsProcessed, setRowsProcessed] = useState(0);

  const onUploadProgress = useCallback((progressEvent: AxiosProgressEvent) => {
    const percentage = Math.floor((progressEvent.progress) ?? 0 * 100);
    setUploadStatus(`Uploading your files (${percentage}%)`);
  }, []);

  const onFile = useCallback(async () => {
    if (!inputRef?.current) {
      return;
    }
    const files = inputRef.current.files ?? [];
    const {data: jobMetadata} = await axios.postForm('http://localhost:3005/upload', {
      'files[]': files,
    }, {
      onUploadProgress,
    });

    let status: keyof typeof MESSAGES = 'TRANSFERRING';
    setUploadStatus(MESSAGES[status]);
    let duration = 0;
    while (status !== 'SUCCESS' && duration < TIMEOUT) {
      await new Promise(resolve => setTimeout(resolve, POLL_INTERVAL));
      duration += POLL_INTERVAL;
      const {data} = await axios.get(`http://localhost:3005/job/${jobMetadata.jobId}`);
      status = data.status as keyof typeof MESSAGES;
      setRowsProcessed(data.rows_ingested);
      setUploadStatus(MESSAGES[status]);
    }
  }, [onUploadProgress]);

  return (
    <div>
      <input
        type='file'
        id='file'
        name='file'
        multiple
        accept='.csv'
        onChange={onFile}
        ref={inputRef}
      />
      {uploadStatus}
      <br/>
      {`Processed ${rowsProcessed} rows`}
    </div>
  )
}

export default App
