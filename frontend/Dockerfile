FROM node:16 as builder

ARG PHASE
RUN echo $PHASE
ENV PHASE=$PHASE

# 작업 폴더를 만들고 npm 설치
RUN mkdir /usr/src/app
WORKDIR /usr/src/app
ENV PATH /usr/src/app/node_modules/.bin:$PATH
COPY ./frontend/package.json /usr/src/app/package.json
# RUN yarn add react-scripts@2.1.3 -g --silent

# 소스를 작업폴더로 복사하고 빌드
COPY ./frontend /usr/src/app
RUN yarn install
RUN yarn build-$PHASE



FROM nginx
# nginx의 기본 설정을 삭제하고 앱에서 설정한 파일을 복사
RUN rm -rf /etc/nginx/conf.d
COPY ./frontend/conf /etc/nginx

# 위에서 생성한 앱의 빌드산출물을 nginx의 샘플 앱이 사용하던 폴더로 이동
COPY --from=builder /usr/src/app/dist /usr/share/nginx/html

# 80포트 오픈하고 nginx 실행
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
