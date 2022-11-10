import React from 'react';
import ReactPlayer from 'react-player';

type Props = {
  setNowPlayTime: React.Dispatch<React.SetStateAction<number>>,
}

const Player = ({ setNowPlayTime }: Props) => {
  const onProgress = (state: any) => {
    // const totalTime = ((1 / state.loaded) * state.loadedSeconds);
    setNowPlayTime(state.playedSeconds * 1000);
    console.log(import.meta.env.VITE_REACT_APP_BACKEND_URL);
  };

  return (
    <ReactPlayer
      url='http://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4'
      controls
      width='100%'
      height='100%'
      onProgress={onProgress}
      progressInterval={500}
    />
  );
};

export default Player;
