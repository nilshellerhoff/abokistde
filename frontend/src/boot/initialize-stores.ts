import { boot } from 'quasar/wrappers';
import { useLocalSettingsStore } from 'stores/local-settings-store';
import { useContentStore } from 'stores/content-store';

export default boot(({}) => {
  const contentStore = useContentStore();
  const localSettingsStore = useLocalSettingsStore();

  contentStore.init();
  localSettingsStore.init();
});
