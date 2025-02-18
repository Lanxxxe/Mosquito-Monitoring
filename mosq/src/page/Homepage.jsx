import { useState, useEffect } from 'react'
import aegypti from '../assets/mosquito/Aedes-aegypti.jpg'
import albopictus from '../assets/mosquito/Aedes-albopictus.jpg'
import niveus from '../assets/mosquito/Aedes-niveus.png'
import vexans from '../assets/mosquito/Aedes-vexans.jpg'
import pipiens from '../assets/mosquito/Culex-pipiens.jpg'
import quintquefasciatus from '../assets/mosquito/Culex-quintquefasciatus.jpg'
import tritaeniorhynchus from '../assets/mosquito/Culex-tritaeniorhynchus.png'
import vishnui from '../assets/mosquito/Culex-vishnui.png'

import dengue from '../assets/danger/dengue.jpg'
import dengueFever from '../assets/danger/dengue-fever.jpeg'
import sylvatic from '../assets/danger/sylvatic-dengue.jpg'
import chikungunya from '../assets/danger/chikungunya.jpg'
import yellowFever from '../assets/danger/yellow-fever.jpg'
import zikaVirus from '../assets/danger/zika-virus.jpg'
import westNile from '../assets/danger/west-nile-virus.jpg'
import japanEncephalitis from '../assets/danger/Japanese-Encephalitis.png'
import stlouis from '../assets/danger/st-louis-encephalitis.jpg'


import axios from 'axios';


const mosquitoImages = {
  "Aedes Aegypti" : aegypti,
  "Aedes Albopictus" : albopictus,
  "Aedes Vexans" : vexans,
  "Aedes Niveus" : niveus,
  "Culex Pipiens" : pipiens,
  "Culex Quinquefasciatus" : quintquefasciatus,
  "Culex Vishnui" : vishnui,
  "Culex Tritaeniorhynchus" : tritaeniorhynchus
}

const diseasesImages = {
  "Dengue" : dengue, 
  "Dengue Fever" : dengueFever,
  "Sylvatic Dengue" : sylvatic, 
  "Chikungunya" : chikungunya, 
  "Yellow Fever" : yellowFever, 
  "Zika Virus" : zikaVirus,
  "West Nile Virus" : westNile,
  "Japanese Encephalitis" : japanEncephalitis,
  "St. Louis Encephalitis" : stlouis
}

const Homepage = () => {
  const [mosquitoData, setMosquitoData] = useState(null);
  const [mostFrequent, setMostFrequent] = useState(null);
  const [otherMosquitoes, setOtherMosquitoes] = useState([]);

  useEffect(() => {
    axios.get('https://mosquito-monitoring.vercel.app/api/detected-stats')
      .then(response => {
        processData(response.data.rows);
      })
      .catch(error => {
        console.error('Error fetching mosquito data:', error);
      });
  }, []);

  const processData = (data) => {
    const mostFrequentMosquito = data.reduce((max, mosquito) => 
      mosquito.detected_count > max.detected_count ? mosquito : max, data[0]);

    const remainingMosquitoes = data
      .filter(mosquito => mosquito.mosquito_name !== mostFrequentMosquito.mosquito_name)
      .sort((a, b) => b.detected_count - a.detected_count);

    setMosquitoData(data);
    setMostFrequent(mostFrequentMosquito);
    setOtherMosquitoes(remainingMosquitoes);
  };

  if (!mosquitoData) {
    return <p>Loading data...</p>;
  }

  const totalDetected = mosquitoData.reduce((sum, mosquito) => sum + mosquito.detected_count, 0);

  return (
    <div className='w-screen min-h-screen bg-slate-200'>
      <div className='py-8'>
        <h1 className='text-center text-5xl font-bold text-blue-500'>MOSMO</h1>
        <p className='text-center font-light italic'>Mosquito Monitoring</p>
      </div>

      <div className='flex flex-wrap items-start justify-start gap-5 p-px md:p-8'>
        <div className='border border-slate-500 min-w-80 md:flex-1 p-5 shadow-md rounded-md'>
          <p className='text-2xl font-bold text-slate-700'>Area is prone to:</p>
          <div className='flex flex-wrap justify-start items-start mt-6'>
            <img className='w-56 mx-auto md:mx-px' src={mosquitoImages[mostFrequent.mosquito_name]} alt='' />
            <div className='w-full'>
              <p className='text-xl md:text-4xl font-semibold text-slate-800 mt-4'>{mostFrequent.mosquito_name}</p>
              <p className='indent-8 mt-4'>{mostFrequent.mosquito_description}</p>

              <div className='mt-3 py-6 flex gap-8 items-center justify-start'>
                <div className='border-2 border-slate-600 p-5 text-center rounded-md'>
                  <p className='text-4xl font-semibold'>{mostFrequent.detected_count}</p>
                  <p className='text-sm'>Total Count</p>
                </div>
                <div className='border-2 border-slate-600 p-5 text-center rounded-md'>
                  <p className='text-4xl font-semibold'>{mostFrequent.detected_percentage}%</p>
                  <p className='text-sm'>Percentage</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className='border border-slate-500 flex-1 p-5 rounded-md'>
            <p className='text-2xl font-bold text-slate-700'>Diseases</p>
            {mostFrequent.diseases.split(', ').map((disease, index) => (
                <div key={index} className='flex items-center justify-start gap-5 p-3 shadow-md mt-4'>
                  <img className='w-25 rounded-md' src={diseasesImages[disease]} alt="diseasesImages[disease]" />
                  <p>{disease}</p>
                </div>
            ))}

        </div>
      </div>

      <p className='ps-8 mt-12 text-lg font-bold text-slate-700'>Other Mosquitoes spotted in the area:</p>
      <div className='mt-5 flex flex-wrap items-stretch justify-start gap-12 p-8'>
          {otherMosquitoes.map((mosquito, index) => (
              <div key={index} className='border border-slate-500 rounded-md flex flex-col p-4 shadow-md'>
                <img className='w-80 h-52 rounded-md mx-auto' src={mosquitoImages[mosquito.mosquito_name]} alt={mosquito.mosquito_name} />
                <p className='text-pretty text-xl text-slate-800 font-bold mt-4'>{mosquito.mosquito_name}</p>
                <p className='indent-4 max-w-80 mt-4'>{mosquito.mosquito_description}</p>
    
                <div className='py-6 flex gap-8 items-center justify-start mt-auto'>
                  <div className='border-2 border-slate-600 p-5 text-center rounded-md'>
                    <p className='text-3xl font-semibold'>{mosquito.detected_count}</p>
                    <p className='text-sm'>Total Count</p>
                  </div>
                  <div className='border-2 border-slate-600 p-5 text-center rounded-md'>
                    <p className='text-3xl font-semibold'>{mosquito.detected_percentage}%</p>
                    <p className='text-sm'>Percentage</p>
                  </div>
                </div>
            </div>
          ))}
      </div>
    </div>
  )
}

export default Homepage
