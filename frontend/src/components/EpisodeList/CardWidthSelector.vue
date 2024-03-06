<template>
  <q-btn-toggle
    v-model="localSettingsStore.episodeListEpisodeCardWidth"
    :options="episodeCardWidthOptions"
    dense
  >
    <template v-slot:small> <q-icon name="r_view_compact" /> </template>
    <template v-slot:medium> <q-icon name="r_view_module" /> </template>
    <template v-slot:large>
      <q-icon name="r_window" />
    </template>
  </q-btn-toggle>
</template>

<script setup lang="ts">
import { useLocalSettingsStore } from 'stores/local-settings-store';

const localSettingsStore = useLocalSettingsStore();

const episodeCardWidthOptions = [
  {
    value: 250,
    slot: 'small',
  },
  {
    value: 300,
    slot: 'medium',
  },
  {
    value: 400,
    slot: 'large',
  },
];
</script>
