import React, { useEffect } from 'react';
import { useRecoilValue } from 'recoil';
import { useNavigate } from 'react-router-dom';
import authState from 'recoil/auth/atom';
import { notification } from 'antd';

type Props = {
    children?: React.ReactNode
}

const PrivateRoute = ({ children }: Props) => {
  const auth = useRecoilValue(authState);
  const navigate = useNavigate();
  useEffect(() => {
    if (!auth.isLoggedIn) {
      notification.error({
        message: '로그인 후 이용해주세요.',
      });
      navigate('/auth/login');
    }
  });
  return (
    <>
      {children}
    </>
  );
};

export default PrivateRoute;
