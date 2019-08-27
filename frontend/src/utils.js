import Vue from 'vue'

Vue.mixin({
  methods: {
    keysToCamel: function (object) {

      var toCamel = (s) => {
        return s.replace(/([-_][a-z])/ig, ($1) => {
          return $1.toUpperCase()
            .replace('-', '')
            .replace('_', '');
        });
      };

      var isArray = function (a) {
        return Array.isArray(a);
      };

      var isObject = function (o) {
        return o === Object(o) && !isArray(o) && typeof o !== 'function';
      };


      if (isObject(object)) {
        const n = {};

        Object.keys(object)
          .forEach((k) => {
            n[toCamel(k)] = this.keysToCamel(object[k]);
          });

        return n;
      } else if (isArray(object)) {
        return object.map((i) => {
          return this.keysToCamel(i);
        });
      }

      return object;
    },
  }
});