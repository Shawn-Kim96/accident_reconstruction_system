import {
  Avatar, Dropdown, Menu, notification,
} from 'antd';
import { Header } from 'antd/lib/layout/layout';
import React from 'react';
import { useSetRecoilState, useRecoilValue } from 'recoil';
import authState from 'recoil/auth/atom';

const AppHeader: React.FC = () => {
  const setAuth = useSetRecoilState(authState);
  const auth = useRecoilValue(authState);

  const handleLogout = () => {
    setAuth({
      isLoggedIn: false,
      accessToken: '',
      info: {
        avatar: '',
        name: '',
        email: '',
      },
    });
    notification.success({
      message: '로그아웃되었습니다.',
      description:
          '고생하셨습니다. 안녕히 가세요.',
    });
  };

  const menu = (
    <Menu
      items={[
        {
          key: 'logout',
          label: 'Logout',
          onClick: handleLogout,
        },
      ]}
    />
  );

  return (
    <Header
      className='site-layout-sub-header-background'
      style={{
        padding: '0 15px', display: 'flex', alignItems: 'center', justifyContent: 'end',
      }}
    >

      <Dropdown overlay={menu}>
        <Avatar style={{ backgroundColor: '#ddd', verticalAlign: 'middle' }} size='large' src={auth.info.avatar}>
          {auth.info.name}
        </Avatar>
      </Dropdown>
    </Header>

  );
};

export default AppHeader;
