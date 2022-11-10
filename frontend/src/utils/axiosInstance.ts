import axios from 'axios';

// axios 인스턴스
const instance = axios.create({
  baseURL: import.meta.env.VITE_REACT_APP_BACKEND_URL!,
  timeout: 15000,
  headers: {
    'Content-Type': 'application/json',
    Authorization: localStorage.getItem('login-token') || '',
  },
});

export const setAxiosHeader = (token?: string) => {
  // eslint-disable-next-line no-unused-expressions
  token
    ? instance.defaults.headers.common.Authorization = token
    : delete instance.defaults.headers.common.Authorization;
};

/**
 * 1. 요청 인터셉터
 */
instance.interceptors.request.use(
  (req) => req,
  (err) => Promise.reject(err),
);

/**
 * 응답 인터셉터
 */
instance.interceptors.response.use(
  (res) => res,
  (error) => Promise.reject(error),
);

export default instance;
