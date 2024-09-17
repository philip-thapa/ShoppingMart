import { combineReducers, configureStore } from "@reduxjs/toolkit";
import authReducer from './authSlice';
import storage from 'redux-persist/lib/storage';
import { persistStore, persistReducer } from 'redux-persist';
import { thunk } from "redux-thunk";

const rootReducer = combineReducers({
    authReducer: authReducer,
})

const persistConfig = {
    key: 'root',
    storage,
};

const persistedReducer = persistReducer(persistConfig, rootReducer);

export const store = configureStore({
    reducer: persistedReducer,
    middleware: (getDefaultMiddleware) =>
      getDefaultMiddleware({
        serializableCheck: {
          ignoredActions: ['persist/PERSIST', 'persist/REHYDRATE'],
        },
      }).concat(thunk)
  });


export const persistor = persistStore(store);