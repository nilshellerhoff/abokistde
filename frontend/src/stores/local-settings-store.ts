import { defineStore } from 'pinia';
import { RemovableRef, useLocalStorage } from '@vueuse/core';

import { Dark } from 'quasar';
import { SubscriptionCategory, UserSubscription } from 'src/types/api';

interface LocalSettingsStore {
  darkMode: RemovableRef<boolean>;
  episodeListMaxNumberOfColumns: RemovableRef<number>;
  episodeListEpisodeCardWidth: RemovableRef<number>;
}

export const useLocalSettingsStore = defineStore('localSettings', {
  state: (): LocalSettingsStore => ({
    darkMode: useLocalStorage('localSettingsdarkMode', false),
    episodeListMaxNumberOfColumns: useLocalStorage(
      'episodeListMaxNumberOfColumns',
      5
    ),
    episodeListEpisodeCardWidth: useLocalStorage(
      'episodelistEpisodeCardWidth',
      300
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
