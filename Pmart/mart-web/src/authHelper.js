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
