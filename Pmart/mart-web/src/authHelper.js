// export const storeToken = (accessToken, refreshToken) => {
//     localStorage.setItem('token', accessToken);
//     localStorage.setItem('refesh', refreshToken);
// }

// export const clearToken = () => {
//     if (localStorage.getItem('token')){
//         localStorage.removeItem('token');
//     }
//     if (localStorage.getItem('refresh')){
//         localStorage.removeItem('refresh');
//     }
// }

// export const getToken = () => {
//     if (localStorage.getItem('token')){
//         return localStorage.getItem('token');
//     }
//     return null;
// }

import Dexie from 'dexie';

const db = new Dexie('mart');
db.version(1).stores({
  tokens: 'id, value'
});

export const setAccessToken = async (token, refresh) => {
  await db.tokens.put({ id: 'token', value: token });
  await db.tokens.put({ id: 'refresh', value: refresh});
};

export const getAccessToken = async () => {
  const record = await db.tokens.get('token');
  return record?.value;
};

export const removeAccessToken = async () => {
  await db.tokens.delete('token');
  await db.tokens.delete('refresh');
};
