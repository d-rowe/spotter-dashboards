import {useEffect, useState, useCallback} from 'react'
import axios from 'axios';

export default function Dashboard() {
    const [embedUrl, setEmbedUrl] = useState('')
    const fetchUrl = useCallback(async () => {
        const response = await axios.get('http://localhost:3005/embed-url');
        setEmbedUrl(response.data);
    }, []);

    useEffect(() => {
        fetchUrl();
    }, [fetchUrl]);


    return (
        <div className='dashboard'>
            <iframe src={embedUrl}/>
        </div>
    )
}