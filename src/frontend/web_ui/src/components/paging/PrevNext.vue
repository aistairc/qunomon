<template>
  <font size="4" class="paging">
    <a
      :href="`?page=${prevPage}`"
      class="prev"
      v-if="confirmedPage > 1"
      @click.prevent="onPrev"
    >&lt; Prev</a>
    <div class="total"> page {{confirmedPage}}/{{totalPage}} </div>
    <a
      :href="`?page=${nextPage}`"
      class="next"
      v-if="confirmedPage < totalPage"
      @click.prevent="onNext"
    >Next &gt;</a>
  </font>
</template>

<script>
export default {
  props: {
    page: {
      type: Number,
      required: true
    },
    totalPage: {
      type: Number,
      required: true
    }
  },
  data() {
    return {
      currentPage: this.page
    };
  },
  computed: {
    confirmedPage: function(){
      if(this.currentPage > this.totalPage){
        this.$emit("change", 1);
        return 1;
      }
      else{
        this.$emit("change", this.currentPage);
        return this.currentPage;
      }
    },
    prevPage: function() {
      return Math.max(this.confirmedPage - 1, 1);
    },
    nextPage: function() {
      return Math.min(this.confirmedPage + 1, this.totalPage);
    }
  },
  methods: {
    onPrev: function() {
      this.currentPage = this.prevPage;
      this.$emit("change", this.currentPage);
    },
    onNext: function() {
      this.currentPage = this.nextPage;
      this.$emit("change", this.currentPage);
    }
  }
};
</script>
<style>
.paging * {
  display: inline;
}
</style>