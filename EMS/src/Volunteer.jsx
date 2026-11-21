import React, { useState,useEffect } from 'react'

function Volunteer() {

  const [data , setData] = useState([])
  const [eventList , setEventList] = useState([])

  function truncateString(str, maxLength) {
  if (str.length > maxLength) {
    return str.substring(0, maxLength - 3) + "...";
  }
  return str;
}

  useEffect(() => {
  const fetchVolunteers = async () => {
  try {
    const response = await fetch(`http://localhost:8000/club`);
    const result = await response.json();
    setData(result);
    setEventList([])
    for(let i=0;i<result.length;i++){
      for(let j=0;j<result[i]["events"].length;j++){
        if(result[i]["events"][j]["need_volunteers"] == true){
          result[i]["events"][j]["club"] = result[i]["club"];
          setEventList(prevItems => [...prevItems , result[i]["events"][j]])
        }
      }
    }
  } catch (error) {
    console.error('Error:', error);
  }
};
     fetchVolunteers();
  }, []);


  return (
    <div className='h-full bg-slate-950'>
      <section className="text-gray-400body-font">
  <div className="container px-5 py-24 mx-auto">
    <div className="flex flex-wrap -m-4">
      {eventList.map((e)=>{
        return( e["need_volunteers"] &&
      <div className="p-4 lg:w-1/3">
        <div className="h-full bg-slate-900 bg-opacity-40 px-8 pt-16 pb-24 rounded-lg overflow-hidden text-center relative">
          <h2 className="tracking-widest text-xs title-font font-medium text-gray-500 mb-1">{e["club"].toUpperCase()}</h2>
          <h1 className="title-font sm:text-2xl text-xl font-medium text-white mb-3">{e["title"]}</h1>
          <p className="leading-relaxed text-gray-500 mb-3">{truncateString(e["desc_volunteer"],150)}</p>
          <a className="text-indigo-400 inline-flex items-center">Apply
            <svg className="w-4 h-4 ml-2" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round">
              <path d="M5 12h14"></path>
              <path d="M12 5l7 7-7 7"></path>
            </svg>
          </a>
          <div className="text-center mt-2 leading-none flex justify-center absolute bottom-0 left-0 w-full py-4">
            <span className="text-gray-500 mr-3 inline-flex items-center leading-none text-sm pr-3 py-1 border-r-2 border-gray-700 border-opacity-50">
              <svg className="w-4 h-4 mr-1" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24">
                <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
                <circle cx="12" cy="12" r="3"></circle>
              </svg>1.2K
            </span>
            <span className="text-gray-500 inline-flex items-center leading-none text-sm">
              <svg className="w-4 h-4 mr-1" stroke="currentColor" stroke-width="2" fill="none" stroke-linecap="round" stroke-linejoin="round" viewBox="0 0 24 24">
                <path d="M21 11.5a8.38 8.38 0 01-.9 3.8 8.5 8.5 0 01-7.6 4.7 8.38 8.38 0 01-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 01-.9-3.8 8.5 8.5 0 014.7-7.6 8.38 8.38 0 013.8-.9h.5a8.48 8.48 0 018 8v.5z"></path>
              </svg>6
            </span>
          </div>
        </div>
      </div>
        )
      })}
    </div>
  </div>
</section>
    </div>
  )
}

export default Volunteer
