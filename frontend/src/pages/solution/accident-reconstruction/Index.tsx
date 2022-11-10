import React, { useState } from 'react';
import {
  ReflexContainer,
  ReflexSplitter,
  ReflexElement,
} from 'react-reflex';
import Map from 'components/Map';

import 'react-reflex/styles.css';
import Player from './components/Player';

const AccidentReconstruction: React.FC = () => {
  const [, setNowPlayTime] = useState<number>(0);
  return (
    <ReflexContainer orientation='vertical'>

      <ReflexElement className='left-pane'>
        <ReflexContainer orientation='horizontal'>
          <ReflexElement className='left-pane'>
            <Player setNowPlayTime={setNowPlayTime} />
          </ReflexElement>
          <ReflexSplitter />
          <ReflexElement className='left-pane' style={{ width: '100%' }} />
        </ReflexContainer>
      </ReflexElement>

      <ReflexSplitter />

      <ReflexElement className='right-pane'>
        <ReflexContainer orientation='horizontal'>
          <ReflexElement className='left-pane'>
            <div className='pane-content' style={{ height: '100%' }}>
              <Map />

            </div>
          </ReflexElement>
          <ReflexSplitter />
          <ReflexElement className='left-pane'>
            <div className='pane-content'>
              Left Pane (resizeable)
            </div>
          </ReflexElement>
        </ReflexContainer>
      </ReflexElement>

    </ReflexContainer>
  );
};

export default AccidentReconstruction;
