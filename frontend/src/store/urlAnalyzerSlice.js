import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';

export const analyzeUrl = createAsyncThunk(
  'urlAnalyzer/analyzeUrl',
  async (url) => {
    const response = await fetch('http://localhost:5001/analyze', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ url }),
    });
    
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.error || 'Failed to analyze URL');
    }
    
    return response.json();
  }
);

const urlAnalyzerSlice = createSlice({
  name: 'urlAnalyzer',
  initialState: {
    url: '',
    question: null,
    options: [],
    status: 'idle', // 'idle' | 'loading' | 'succeeded' | 'failed'
    error: null,
    selectedOption: null,
  },
  reducers: {
    setUrl: (state, action) => {
      state.url = action.payload;
    },
    setSelectedOption: (state, action) => {
      state.selectedOption = action.payload;
    },
    resetAnalysis: (state) => {
      state.question = null;
      state.options = [];
      state.status = 'idle';
      state.error = null;
      state.selectedOption = null;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(analyzeUrl.pending, (state) => {
        state.status = 'loading';
        state.error = null;
      })
      .addCase(analyzeUrl.fulfilled, (state, action) => {
        state.status = 'succeeded';
        state.question = action.payload.question;
        state.options = action.payload.options;
      })
      .addCase(analyzeUrl.rejected, (state, action) => {
        state.status = 'failed';
        state.error = action.error.message;
      });
  },
});

export const { setUrl, setSelectedOption, resetAnalysis } = urlAnalyzerSlice.actions;
export default urlAnalyzerSlice.reducer;