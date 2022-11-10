import React from 'react';
import { Menu } from 'antd';
import { Link } from 'react-router-dom';

const AppMenu: React.FC = () => (
  <Menu
    theme='dark'
    mode='inline'
    defaultSelectedKeys={['']}
  >
    <Menu.Item key='home'>
      <Link to='/' className='nav-text'>Home</Link>
    </Menu.Item>
    <Menu.Item key='accident-reconstruction'>
      <Link to='/accident-reconstruction' className='nav-text'>Accident Reconstruction</Link>
    </Menu.Item>
  </Menu>
);

export default AppMenu;
