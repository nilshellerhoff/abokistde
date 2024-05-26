<template>
  <div v-if="props.episodes.length == 0">
    <q-item>
      <q-item-section>
        <q-item-label>No Episodes found</q-item-label>
      </q-item-section>
    </q-item>
  </div>

  <EpisodeListItem
    v-for="episode in props.episodes"
    :key="episode.id"
    :episode="episode"
    :width="200"
  />
</template>

<script setup lang="ts">
import { Episode } from 'src/types/api';
import EpisodeListItem from 'components/EpisodeList/EpisodeListItem.vue';

interface Props {
  episodes: Episode[];
}

const props = defineProps<Props>();
</script>
