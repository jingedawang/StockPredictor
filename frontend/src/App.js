import { Layout } from 'antd';

import './App.css';
import { Board  } from './component/Board';
import { Query } from './component/Query';
import { Recommend } from './component/Recommend'

const { Header, Footer, Content, Sider } = Layout;

function App() {
  return (
    <div className="app">
      <Layout>
          <Header className='head'>Stock Prediction</Header>
          <Content className='content'>
            <Query />
            <Board />
          </Content>
          <Sider className='sider'>
            <Recommend />
          </Sider>
        <Footer className='footer'>
          <span>Author @Yifan Zou</span>
          <a href='mailto: wjg172184@163.com'>Email</a>
          <a href='https://github.com/jingedawang/StockPredictor' target="_blank">GitHub</a>
        </Footer>
      </Layout>
    </div>
  );
}

export default App;
