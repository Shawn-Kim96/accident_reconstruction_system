import { atom } from 'recoil';
import localStorageEffect from 'recoil/effects/localStorageEffect';

const authState = atom({
  key: 'authState',
  default: {
    isLoggedIn: false,
    accessToken: '',
    info: {
      avatar: '',
      name: '',
      email: '',
    },
  },
  effects: [localStorageEffect('authState')],
});

export default authState;
