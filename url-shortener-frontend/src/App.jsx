import { useState } from 'react';
import './App.css'

function App() {
  const [url, setUrl] = useState('');
  const [short, setShort] = useState(null);
  const submit = async e => {
    e.preventDefault();
    const r = await fetch(`${import.meta.env.VITE_API_URL}/links`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ url })
    });
    if (!r.ok) {
      throw new Error(`Request failed with status ${r.status}`);
    }

    const data = await r.json();
    setShort(data.short_url);
  };

  return (
    <div className='url-container'>
      <form id='form-short'  onSubmit={submit}>

        <input
          className='input-form'
          value={url}
          onChange={e => setUrl(e.target.value)}
          placeholder='enter your URL' />
        <div className='button'>
          <button className='submit-bttn'>
          Shorten
        </button>
        </div>
        
      </form>
      {short && <p>Your short link: <a href={short}>{short}</a></p>}
    </div>
  )
}

export default App
