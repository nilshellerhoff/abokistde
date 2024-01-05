<template>
  <div class="q-pa-md row justify-between">
    <div class="col-auto q-ma-lg order-xs-first">
      <q-avatar style="width: 80px; height: 80px">
        <q-img :src="props.channel?.thumbnail_url" />
      </q-avatar>
    </div>
    <div class="col-sm col-xs-12 self-center order-xs-last">
      <q-item-label overline class="text-subtitle-2">{{
        props.channel?.provider.name
      }}</q-item-label>
      <q-item-label class="text-h4">{{ props.channel?.name }}</q-item-label>
    </div>
    <div class="col-auto self-center">
      <q-btn
        v-if="props.channel?.url"
        color="primary"
        label="Go to channel"
        icon="open_in_new"
        :href="props.channel?.url"
        target="_blank"
        rel="noopener"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { PublishingChannel } from 'src/types/api';

interface Props {
  channel?: PublishingChannel;
}

const props = defineProps<Props>();

console.log(process.env.VUE_APP_SOMEKEY);
</script>

<style>
@media (max-width: 600px) {
  .order-xs-last {
    order: 10000;
  }

  .order-xs-first {
    order: -10000;
  }
}

@media (min-width: 600px) {
  .order-xs-last {
  }
  .order-xs-first {
  }
}
</style>
