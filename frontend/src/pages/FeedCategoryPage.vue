<template>
  <q-page>
    <span v-if="categoryId">
      <episode-list
        :episode-api-params="{
          is_subscribed: true,
          category_id: categoryId,
        }"
      />
    </span>
  </q-page>
</template>

<script setup lang="ts">
import EpisodeList from 'components/EpisodeList/EpisodeList.vue';
import { useRoute } from 'vue-router';
import { ref, watch } from 'vue';

const route = useRoute();

const categoryId = ref(route.params.id);

watch(
  () => route.params.id,
  (id) => {
    categoryId.value = id;
  }
);
</script>
