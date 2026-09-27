const API=import.meta.env.VITE_API_URL||'http://127.0.0.1:8000/api';
async function request(path,options={}){const res=await fetch(API+path,options); if(!res.ok){throw new Error(await res.text()||'API request failed')} return res.json()}
export const getSummary=()=>request('/dashboard/summary?user_id=demo-user');
export const getTransactions=()=>request('/transactions?user_id=demo-user');
export const getForecast=()=>request('/analytics/forecast?user_id=demo-user&days=30');
export const sendChat=(message)=>request('/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({user_id:'demo-user',message})});
export const importCsv=(file)=>{const f=new FormData();f.append('file',file);return request('/transactions/import-csv?user_id=demo-user',{method:'POST',body:f})};
