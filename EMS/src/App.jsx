import { useState,useEffect } from 'react'
import './App.css'
import events from './assets/events.json'

function App() {
  const [data, setData] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

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
    <div className='min-h-screen bg-slate-950'>
      {data.map((ev)=>{
        return(
          <div className="parent">
      <section className="text-gray-400 bg-slate-950 body-font overflow-hidden">
        <div className="container px-5 py-10 mx-auto shadow-lg shadow-green-500/20 my-5 rounded-lg">
          <div className="-my-8 divide-y-2 divide-gray-800">
            <div className="py-8 flex flex-wrap md:flex-nowrap">
              <div className="md:w-64 md:mb-0 mb-6 flex-shrink-0 flex flex-col">
                <span className="font-semibold title-font text-green-500 bg-gray-800 px-4 py-1 rounded-lg w-fit">{ev.club}</span>
                <span className="mt-1 text-gray-500 text-sm">{ev.date}</span>
              </div>
              <div className="md:flex-grow">
                <h2 className="text-2xl font-medium text-white title-font mb-2">{ev.title}</h2>
                <p className="leading-relaxed">Venue : {ev.venue}</p>
                <p className="leading-relaxed my-2">Guests : {ev.guests.map((e)=>{return(
                  <span className="font-semibold title-font mx-2 bg-gray-800 px-2 py-1 rounded-lg w-fit">{e}</span>
                )})}</p>
                <a className="text-green-400 inline-flex items-center mt-4">Register
                  <svg className="w-4 h-4 ml-2" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round">
                    <path d="M5 12h14"></path>
                    <path d="M12 5l7 7-7 7"></path>
                  </svg>
                </a>
              </div>
            </div>
          </div>
        </div>
      </section>
      </div>
        )
      })}
      
    </div>
  )
}

export default App
