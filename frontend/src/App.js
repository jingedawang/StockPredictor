import { Layout } from 'antd';

import './App.css';
import { Board  } from './component/Board';
import { Query } from './component/Query';

const { Header, Footer, Content } = Layout;

function App() {
  return (
    <div className="app">
      <Layout>
          <Header className='head'>Header</Header>
          <Content className='content'>
            <Query />
            <Board />
          </Content>
        <Footer className='footer'>Footer</Footer>
      </Layout>
     
    </div>
  );
}

export default App;
