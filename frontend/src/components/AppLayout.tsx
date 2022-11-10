import React from 'react';
import {
  Layout,
} from 'antd';
import { Outlet } from 'react-router-dom';
import AppMenu from './AppMenu';
import AppHeader from './AppHeader';

const {
  Footer, Sider, Content,
} = Layout;

const AppLayout: React.FC = () => (
  <Layout style={{ height: '100vh' }}>
    <Sider
      breakpoint='lg'
      collapsedWidth='0'
    >
      <div className='logo'>FII Solutions</div>
      <AppMenu />
    </Sider>
    <Layout>
      <AppHeader />
      <Content style={{ margin: '10px', display: 'flex' }}>
        <Outlet />
      </Content>
      <Footer style={{ textAlign: 'center' }}>FII Solutions ©2022 Created by Fleet AIoT Team</Footer>
    </Layout>
  </Layout>
);

export default AppLayout;
