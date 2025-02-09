import React from 'react'
import mosquito1 from '../assets/mosquitos/Aedes genus/Aedes 1(1).jpg'
import mosquito3 from '../assets/mosquitos/Aedes genus/Aedes 3(4).jpg'
import mosquito2 from '../assets/mosquitos/Aedes genus/Aedes 2(2).jpg'
import dengue from '../assets/danger/dengue-fever.jpeg'
import japencep from '../assets/danger/Japanese-Encephalitis.png'


const Homepage = () => {
  return (
    <div className='w-full min-h-screen bg-slate-200 '>
        <div className='py-12'>
            <h1 className='text-center text-5xl font-bold text-blue-500'>MOSMO</h1>
            <p className='text-center font-light italic'>Mosquito Monitoring</p>
        </div>
        <div className='flex items-start justify-start gap-5 p-8'>
          <div className='flex-1 p-5 shadow-xl rounded-md'>
            <p className='text-2xl font-bold text-slate-700'>Area is prone to:</p>
            <div className='flex justify-start items-start gap-12 mt-6'>

              <img className='w-56' src={mosquito3} alt="Mosquito" />
              <div className='w-full '>
                <p className='text-5xl font-semibold text-slate-800'>Aedes vexans</p>
                <p className='indent-8 mt-8'>a mosquito species native to China, also carries mosquito-borne
                    viruses, such as dengue fever virus and Japanese encephalitis virus, but research
                    on this mosquito has been inadequate.
                </p>
              </div>
            </div>

          </div>
          <div className='flex-1 p-5 rounded-md'>
            <p className='text-2xl font-bold text-slate-700'>Diseases</p>
              <div className='flex items-center justify-start gap-5 p-3 shadow2xl mt-5'>
                <img className='w-25 rounded-md' src={dengue} alt="Dengue Fever" />
                <p>Dengue Fever</p>
              </div>
              <div className='flex items-center justify-start gap-5 p-3 shadow-xl mt-5'>
                <img className='w-25 h-25 rounded-md' src={japencep} alt="Dengue Fever" />
                <p>Japanese Encephalitis</p>
              </div>
          </div>
        </div>
        <p className='ps-8 mt-5 text-lg font-bold text-slate-700'>Other Mosquitos spotted in the area:</p>
        <div className='mt-5 flex items-start justify-start gap-5 p-8'>
          <div className='flex flex-col gap-4 p-4 shadow-xl'>
            <img className='w-80 h-52 rounded-2' src={mosquito1} alt="" />
            <p className='text-pretty text-xl text-slate-800 font-bold'>Aedes aegypti</p>  
            <p className='indent-4 max-w-80'>
              Aedes aegypti is a mosquito species that is known for its capability in
              transmitting diseases such as dengue, chikungunya, yellow fever, and Zika virus. It
              highlights the importance of understanding how environmental factors influence the
              traits of mosquitoes
              </p>         
          </div>
          <div className='flex flex-col gap-2 p-4 shadow-xl'>
            <img className='w-80 h-52 rounded-2' src={mosquito2} alt="" />
            <p className='text-pretty text-xl text-slate-800 font-bold'>Aedes albopictus</p>  
            <p className='indent-4 max-w-80'>
            Aedes albopictus belongs to the aedes genus of mosquitoes, they can
            transmit several diseases through biting their hosts which includes dengue fever,
            chikungunya, and zika virus. Aedes albopictus continues to spread health risks to
            people living in tropical and subtropical regions, as well as in cold weather.
              </p>         
          </div>
        </div>
    </div>
  )
}

export default Homepage