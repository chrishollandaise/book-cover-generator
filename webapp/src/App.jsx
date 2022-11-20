import { useState, useEffect} from 'react'
import logo from './assets/logo.svg'
import './App.css'

function Book(props) {
  const { book , styles } = props;

  const [isLoaded, setIsLoaded] = useState(false);
  const [plate, setPlate] = useState("");
  const [style, setStyle] = useState("");
  const [passage, setPassage] = useState("");
  
  const onChange = (event, f) => {
    f(event.target.value);
  };

  return <div className="book">
    <h2>{book.title}</h2>
    <p>{book.author}</p>
    <img className="plate" style={{"display": !isLoaded ? "None" : "Block"}} src={plate} alt="Book illustration" />

    <form>
      <fieldset className="passage-fieldset">
        <legend className='accent'><strong>Select a passage.</strong></legend>
        {book.passages.map(passage => {
            return(
            <div key={`${passage.text}`} className="passage-selection">
              <input type='radio' id={`${passage.chapter}-${passage.text[0]}`} name="passage" onChange={(e) => {onChange(e, setPassage)}} value={passage.text} required/>
              <label htmlFor={`${passage.chapter}-${passage.text[0]}`}>{passage.text}</label>
            </div>
            )
        })}
      </fieldset>
      <div>
        <label htmlFor="style">Select a style: </label>
        <select name="style" id="style" onChange={(e) => {onChange(e, setStyle)}} required>
          <option value="">--</option>
          {styles.map(style => {
            return <option key={style[0]} value={style}>{style}</option>
          })}
        </select>
      <button type="submit" onClick={(e) => {
        e.preventDefault();
        
        if (style && passage) {
          setIsLoaded(false);
          fetch('http://localhost:8000/imagine', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            "passage": passage,
            "style": style
          }),
        })
        .then(response => response.json())
        .then(data => {
          const id = data['id'];
          fetch(`http://localhost:8000/plates/${id}`)
          .then(res => setPlate(res.url))
          setIsLoaded(true);
        })
      }
      }}>
        Generate
      </button>
      </div>
    </form>
  </div>
}

function App() {
  const [error, setError] = useState(null);
  const [isLoaded, setIsLoaded] = useState(false);
  const [books, setBooks] = useState([]);
  const [styles, setStyles] = useState([]);

  useEffect(() => {
    (async () => {
      await fetch("http://localhost:8000/books")
      .then(res => res.json())
      .then(
        (result) => {
          setBooks(result['result']);
        },
        (error) => {
          setIsLoaded(true);
          setError(error);
        }
      )

      await fetch("http://localhost:8000/styles")
      .then(res => res.json())
      .then(
        (result) => {
          setStyles(result['styles']);
        },
        (error) => {
          setIsLoaded(true);
          setError(error);
        }
      )
        if(!error)
          setIsLoaded(true);
      })()
    }, [])

  if(error) {
    return <div>Error!</div>
  } else if (!isLoaded) {
    return <div>Loading...</div>
  } else {
    return (
    <div>
      <img src={logo} className="logo" alt="A phoenix rising from a book" />
      <ul>
        {books.map(book => {
          return (
            <div key={book.author}>
              <Book book={book} styles={styles}/>
              <hr />
            </div> 
          )
        })}
      </ul>
    </div>
    )
  }  
}

export default App
