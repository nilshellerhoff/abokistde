import { boot } from 'quasar/wrappers';
import { useLocalSettingsStore } from 'stores/local-settings-store';

export default boot(({}) => {
  const localSettingsStore = useLocalSettingsStore();
  localSettingsStore.init();
});
