import React from 'react';
import styled from 'styled-components';

type Props = {
  children: React.ReactNode
}

const StyledFlexColumnLayout = styled.div`
  display: flex;
  flex-direction: column;
  width: 100%;
`;

const FlexColumnLayout = ({ children }: Props) => (
  <StyledFlexColumnLayout>
    {children}
  </StyledFlexColumnLayout>

);

export default FlexColumnLayout;
