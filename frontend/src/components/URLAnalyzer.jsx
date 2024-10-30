import React, { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { Search, Loader2 } from 'lucide-react';
import { Alert } from '@welcome-ui/alert';
import { analyzeUrl, setUrl, setSelectedOption, resetAnalysis } from '../store/urlAnalyzerSlice';

export default function URLAnalyzer() {
  const dispatch = useDispatch();
  const {
    url,
    question,
    options,
    status,
    error,
    selectedOption
  } = useSelector((state) => state.urlAnalyzer);

  // Effect to reset the form after selection
  useEffect(() => {
    let timeoutId;
    if (selectedOption !== null) {
      timeoutId = setTimeout(() => {
        dispatch(resetAnalysis());
        dispatch(setUrl(''));
        dispatch(setSelectedOption(null));
      }, 1000); // Wait 1 second before resetting
    }
    return () => {
      if (timeoutId) {
        clearTimeout(timeoutId);
      }
    };
  }, [selectedOption, dispatch]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (url.trim()) {
      dispatch(resetAnalysis());
      dispatch(analyzeUrl(url.trim()));
    }
  };

  const handleOptionSelect = (index) => {
    dispatch(setSelectedOption(index));
  };

  return (
    <div className="min-h-screen bg-gray-50 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md mx-auto">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Website Intent Analyzer</h1>
          <p className="mt-2 text-gray-600">
            Enter a website URL to analyze visitor intent
          </p>
        </div>

        {/* URL Input Form */}
        <form onSubmit={handleSubmit} className="mb-8">
          <div className="flex gap-2">
            <div className="relative flex-grow">
              <input
                type="url"
                value={url}
                onChange={(e) => dispatch(setUrl(e.target.value))}
                placeholder="https://example.com"
                required
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 pl-4"
              />
            </div>
            <button
              type="submit"
              disabled={status === 'loading'}
              className="inline-flex items-center px-4 py-2 border border-transparent rounded-lg shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 disabled:opacity-50"
            >
              {status === 'loading' ? (
                <Loader2 className="w-5 h-5 animate-spin" />
              ) : (
                <Search className="w-5 h-5" />
              )}
            </button>
          </div>
        </form>

        {/* Error Message */}
        {error && (
          <Alert variant="destructive" className="mb-6">
            {/* <AlertDescription>{error}</AlertDescription> */}
          </Alert>
        )}

        {/* Results */}
        {question && (
          <div className="bg-white rounded-lg shadow p-6 space-y-4">
            <h2 className="text-xl font-semibold text-gray-900 mb-4">
              {question}
            </h2>
            <div className="space-y-3">
              {options.map((option, index) => (
                <button
                  key={index}
                  className={`w-full text-left px-4 py-3 border rounded-lg transition-colors ${
                    selectedOption === index
                      ? 'border-blue-500 bg-blue-50'
                      : 'border-gray-200 hover:bg-gray-50'
                  }`}
                  onClick={() => handleOptionSelect(index)}
                >
                  <span className="font-medium text-gray-900">
                    {String.fromCharCode(65 + index)}.
                  </span>{' '}
                  <span className="ml-2 text-gray-700">{option}</span>
                </button>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}