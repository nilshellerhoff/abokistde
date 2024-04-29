<template>
  <q-item
    clickable
    v-ripple
    :active="$route.name === 'search'"
    active-class="active"
    to="/search"
  >
    <q-item-section avatar>
      <q-icon name="search" />
    </q-item-section>
    <q-item-section>Search</q-item-section>
  </q-item>

  <q-item
    clickable
    v-ripple
    :active="$route.name === 'favorites'"
    active-class="active"
    to="/favorites"
  >
    <q-item-section avatar>
      <q-icon name="favorite" />
    </q-item-section>
    <q-item-section>Favorites</q-item-section>
  </q-item>

  <q-item
    clickable
    v-ripple
    :active="$route.name === 'feed'"
    active-class="active"
    to="/"
  >
    <q-item-section avatar>
      <q-icon name="subscriptions" />
    </q-item-section>
    <q-item-section>Feed</q-item-section>
  </q-item>

  <div style="height: calc(100% - 104px - 46px)">
    <ChannelList />
  </div>
  <q-separator />
  <q-item>
    <q-btn
      label="Github"
      icon="img:https://github.githubassets.com/favicons/favicon.png"
      href="https://github.com/nilshellerhoff/abokistde"
      target="_blank"
    />
  </q-item>
</template>

<script setup lang="ts">
import ChannelList from 'components/ChannelList.vue';
import { useRoute } from 'vue-router';

const route = useRoute();

console.log(route.name);
</script>

<style scoped>
.active {
  background-color: #00000022;
}
</style>
