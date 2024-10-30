import { Provider } from 'react-redux';
import { store } from './store/store';
import URLAnalyzer from './components/URLAnalyzer';

function App() {
  return (
    <Provider store={store}>
      <URLAnalyzer />
    </Provider>
  );
}

export default App;