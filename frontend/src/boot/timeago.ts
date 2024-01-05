import timeago from 'vue-timeago3';
import { boot } from 'quasar/wrappers';

export default boot(({ app }) => {
  app.use(timeago);
});
