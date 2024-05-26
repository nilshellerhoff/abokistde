<template>
  <div v-if="props.episodes.length == 0">
    <q-item>
      <q-item-section>
        <q-item-label>No Episodes found</q-item-label>
      </q-item-section>
    </q-item>
  </div>

  <div
    class="q-gutter-md"
    style="display: flex; justify-content: center; flex-wrap: wrap; width: 100%"
  >
    <EpisodeListItem
      v-for="episode in props.episodes"
      :key="episode.id"
      :episode="episode"
      :width="200"
    />
  </div>
</template>

<script setup lang="ts">
import { Episode } from 'src/types/api';
import EpisodeListItem from 'components/EpisodeList/EpisodeListItem.vue';

interface Props {
  episodes: Episode[];
}

const props = defineProps<Props>();
</script>
