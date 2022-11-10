import React from 'react';
import styled from 'styled-components';

type Props = {
  children: React.ReactNode
}

const StyledFlexRowLayout = styled.div`
  display: flex;
  flex-direction: row;
  width: 100%;
`;

const FlexRowLayout = ({ children }: Props) => (
  <StyledFlexRowLayout>
    {children}
  </StyledFlexRowLayout>

);
export default FlexRowLayout;
