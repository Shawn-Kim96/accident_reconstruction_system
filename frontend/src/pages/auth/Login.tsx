import React from 'react';
import GoogleLogin from 'react-google-login';
import { useNavigate } from 'react-router-dom';
import authState from 'recoil/auth/atom';
import { useSetRecoilState } from 'recoil';
import { Divider, notification } from 'antd';
import styled from 'styled-components';
import { setAxiosHeader } from '../../utils/axiosInstance';

type Props = {}

// eslint-disable-next-line no-empty-pattern
const Login: React.FC<Props> = ({}) => {
  const setAuth = useSetRecoilState(authState);
  const navigate = useNavigate();
  const handleSuccessLogin = (res: any) => {
    setAuth({
      isLoggedIn: true,
      accessToken: res.accessToken,
      info: {
        avatar: res.profileObj.imageUrl,
        name: `${res.profileObj.familyName}${res.profileObj.givenName}`,
        email: res.profileObj.email,
      },
    });
    setAxiosHeader(res.accessToken);
    localStorage.setItem('login-token', res.accessToken);
    notification.success({
      message: '로그인되었습니다.',
      description: `${res.profileObj.familyName}${res.profileObj.givenName}님, 반가워요!`,
    });
    navigate('/');
  };
  const handleFailureLogin = () => {
    notification.error({
      message: '로그인에 실패했습니다.',
    });
  };
  const clientId = '277311189783-dja9p1f20khg2jmln0bq1p1flp1vsqts.apps.googleusercontent.com';
  const PageContainer = styled.div`
    display: flex;
    background-color: #f0f2f5;
    width: 100%;
    height: 100vh;
    justify-content: center;
    align-items: center;
  `;
  const LoginCard = styled.div`
    background-color: #fff;
    border-radius: 10px;
    box-shadow: 4px 3px 6px -1px rgba(0,0,0,0.1);
    padding: 40px 15px 10px;
    width: 100%;
    max-width: 480px;
    text-align: center;
  `;
  const LoginButton = styled.button`
    margin: 0 auto;
    display: flex;
    align-items: center;
    border-radius: 10px;
    padding: 6px 40px;
    box-shadow: 4px 3px 6px -1px rgba(0,0,0,0.2);
    background-color: #fff;
    border: 0;
    font-size: 16px;
    transition: all 300ms;
    :hover {
      cursor: pointer;
      background-color: #f2efff;
    }
  `;

  return (
    <PageContainer>
      <div style={{
        display: 'flex', width: '100%', maxWidth: 1024, height: '600px', justifyContent: 'center', alignItems: 'center',
      }}
      >
        <LoginCard>
          <div>
            <img src='/images/cosmos-logo.png' alt='logo' width={220} />
          </div>
          <div style={{ marginTop: 30 }}>
            <GoogleLogin
              clientId={clientId}
              responseType='id_token'
              render={(renderProps) => (
                <LoginButton className='font-ibmplex' type='button' onClick={renderProps.onClick} disabled={renderProps.disabled}>
                  구글 계정으로 로그인
                </LoginButton>
              )}
              onSuccess={handleSuccessLogin}
              onFailure={handleFailureLogin}
            />
          </div>
          <Divider />
          <div style={{ color: '#ccc' }}>
            FII Solutions는 @42dot.ai 구글 계정으로만 접속이 가능합니다.
          </div>
        </LoginCard>
      </div>
    </PageContainer>
  );
};

export default Login;
