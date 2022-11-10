import React from 'react';
import styled from 'styled-components';

type Props = {
  children: React.ReactNode
}

const StyledScrollLayout = styled.div`
  width: 100%;
  overflow-y: auto;
`;

const ScrollLayout = ({ children }: Props) => (
  <StyledScrollLayout>
    {children}
  </StyledScrollLayout>

);

export default ScrollLayout;
