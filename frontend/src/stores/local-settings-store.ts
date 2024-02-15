import { defineStore } from 'pinia';
import { useLocalStorage } from '@vueuse/core';

import { Quasar, Platform, Dark } from 'quasar';

export const useLocalSettingsStore = defineStore('localSettings', {
  state: () => ({
    darkMode: useLocalStorage('localSettingsdarkMode', false),
    episodeListMaxNumberOfColumns: useLocalStorage(
      'episodeListMaxNumberOfColumns',
      5
    ),
  }),
  getters: {
    isDarkMode: (state) => state.darkMode,
  },
  actions: {
    init() {
      Dark.set(this.darkMode);
    },
    toggleDarkMode() {
      Dark.toggle();
      this.darkMode = Dark.isActive;
    },
  },
});
