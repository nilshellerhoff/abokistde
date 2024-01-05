export const getBaseApiUrl = () => {
  const djangoHost = getDjangoHost();
  return `${djangoHost}/api`;
};

export const getLoginUrl = () => {
  const djangoHost = getDjangoHost();
  return `${djangoHost}/accounts/login/`;
};

export const getDjangoHost = () => {
  const location = window.location;
  if (process.env.DEV) {
    return `${location.protocol}//${location.hostname}:8000`;
  }
  return `${location.protocol}//${location.host}`;
};
