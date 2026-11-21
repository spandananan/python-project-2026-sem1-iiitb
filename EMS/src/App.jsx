import { useState,useEffect } from 'react'
import './App.css'
import events from './assets/events.json'
import Login from './login.jsx';
import AddEvent from './AddEvent.jsx';
import DeleteEvent from './DeleteEvent.jsx';
import UpdateEvent from './UpdateEvent.jsx';
import Home from './Home.jsx';
import Volunteer from './Volunteer.jsx';
import { BrowserRouter , Link , Routes , Route } from 'react-router-dom';


function App() {
  const [isOpen , setIsOpen] = useState(false);
  const [isOpenClub , setIsOpenClub] = useState(false);
  const[loading , setLoading] = useState(false);
  const[data , setData] = useState(false);
  const[error , setError] = useState(false);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch('http://localhost:8000/events');
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        const result = await response.json();
        setData(result);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  return (
    <>
    <BrowserRouter>
    <header className="text-gray-400 bg-gray-900 body-font">
          <div className="container mx-auto flex flex-wrap p-5 flex-col md:flex-row items-center">
            <a className="flex title-font font-medium items-center text-white mb-4 md:mb-0">
              <svg xmlns="http://www.w3.org/2000/svg" fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" className="w-10 h-10 text-white p-2 bg-green-500 rounded-full" viewBox="0 0 24 24">
                <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"></path>
              </svg>
              <span className="ml-3 text-xl">EMS</span>
            </a>
            <nav className=" md:mr-auto md:ml-4 md:py-1 md:pl-4 md:border-l md:border-gray-700 flex items-center text-base justify-center">
              {/* <Link to="/" className="mr-5 hover:text-white">Home</Link>
              <Link to="/AddEvent" className="mr-5 hover:text-white">Add Event</Link>
              <Link to="/DeleteEvent" className="mr-5 hover:text-white">Remove Event</Link>
              <Link to="/UpdateEvent" className="mr-5 hover:text-white">Update Event</Link> */}
      <Link to="/" className="mr-5 hover:text-white">Home</Link>
              <div className="dropdown mr-5">
      <button onClick={() => setIsOpen(!isOpen)}>
        Events
      </button>
      {isOpen && (
        <ul className="dropdown-menu absolute z-20">
          <li className=' p-2 w-full bg-slate-800 hover:bg-slate-700 rounded-t-md'>
            <Link to="/AddEvent" onClick={() => setIsOpen(false)}>
              Add Event
            </Link>
          </li>
          <li className=' p-2 w-full bg-slate-800 hover:bg-slate-700'>
            <Link to="/UpdateEvent" onClick={() => setIsOpen(false)}>
              Update Event
            </Link>
          </li>
          <li className=' p-2 w-full bg-slate-800 hover:bg-slate-700 rounded-b-md'>
            <Link to="/DeleteEvent" onClick={() => setIsOpen(false)}>
              Remove Event
            </Link>
          </li>
        </ul>
      )}
      </div>
       <div className="dropdown mr-5">
      <button onClick={() => setIsOpenClub(!isOpenClub)}>
        Club
      </button>
      {isOpenClub && (
        <ul className="dropdown-menu absolute z-20">
          <li className=' p-2 w-full bg-slate-800 hover:bg-slate-700 rounded-t-md'>
            <Link to="/AddClub" onClick={() => setIsOpenClub(false)}>
              Add Club
            </Link>
          </li>
          <li className=' p-2 w-full bg-slate-800 hover:bg-slate-700 rounded-b-md'>
            <Link to="/Analytics" onClick={() => setIsOpenClub(false)}>
              View Analytics
            </Link>
          </li>
        </ul>
      )}
    </div>
    <Link to="/Volunteer"  className="mr-5 hover:text-white" onClick={() => setIsOpenClub(false)}>
             Volunteer
            </Link>
            </nav>
            {/* <Link to="/login">
            <button className="inline-flex items-center bg-gray-800 border-0 py-1 px-3 focus:outline-none hover:bg-gray-700 rounded text-base mt-4 md:mt-0">Sign in 
            <svg fill="none" stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" className="w-4 h-4 ml-1" viewBox="0 0 24 24">
            <path d="M5 12h14M12 5l7 7-7 7"></path>
            </svg>
            </button>
            </Link> */}
            
          </div>
        </header>
        {/* <Routes>
        <Route path="/" element={<App />} />
        <Route path="/AddEvent" element={<AddEvent />} />
        <Route path="/DeleteEvent" element={<DeleteEvent />} />
        <Route path="/UpdateEvent" element={<UpdateEvent />} />
        <Route path="/login" element={<Login />} />
        </Routes> */}
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/AddEvent" element={<AddEvent />} />
          <Route path="/DeleteEvent" element={<DeleteEvent />} />
          <Route path="/UpdateEvent" element={<UpdateEvent />} />
          <Route path="/Volunteer" element={<Volunteer />} />
          <Route path="/login" element={<Login />} />
        </Routes>
      </BrowserRouter>
      </>
  )
}

export default App
