import './App.css'

function App() {

  return (
    <form method="post" enctype="multipart/form-data" action="http://localhost:3005/upload">
      <div>
        <label for="file">Choose file to upload</label>
        <br />
        <input type="file" id="file" name="file" multiple />
      </div>
      <div>
        <button>Submit</button>
      </div>
    </form>
  )
}

export default App
