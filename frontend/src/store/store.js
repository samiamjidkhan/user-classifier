import { configureStore } from '@reduxjs/toolkit';
import urlAnalyzerReducer from './urlAnalyzerSlice';

export const store = configureStore({
  reducer: {
    urlAnalyzer: urlAnalyzerReducer,
  },
});