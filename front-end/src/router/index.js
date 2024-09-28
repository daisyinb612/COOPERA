import { createRouter, createWebHashHistory } from "vue-router";
import HomePage from "../views/homepage.vue";
import InputLogLine from "../views/InputLogLine.vue";
import PageOne from "../views/pageone.vue";
import PageTwo from "../views/pagetwo.vue";
import PageThree from "../views/pagethree.vue";
import PageFour from "../views/pagefour.vue";
import RenderScript from "../views/renderscript.vue";

const routes = [
  {
    path: "/",
    redirect: "/home",
  },
  {
    path: "/home",
    component: HomePage,
    children: [
      {
        path: "inputlogline",
        name: "LogLine",
        component: InputLogLine,
        meta: {
          keepAlive: true,
        },
      },
      {
        path: "pageone",
        name: "PageOne",
        component: PageOne,
        meta: {
          keepAlive: true,
        },
      },
      {
        path: "pagetwo",
        name: "PageTwo",
        component: PageTwo,
        meta: {
          keepAlive: true,
        },
      },
      {
        path: "pagethree",
        name: "PageThree",
        component: PageThree,
        meta: {
          keepAlive: true,
        },
      },
      {
        path: "pagefour",
        name: "PageFour",
        component: PageFour,
        meta: {
          keepAlive: true,
        },
      },
      {
        path: "renderscript",
        name: "RenderScript",
        component: RenderScript,
        meta: {
          keepAlive: true,
        },
      },
    ],
  },
];

const router = createRouter({
  // eslint-disable-next-line no-undef
  history: createWebHashHistory(process.env.BASE_URL),
  routes,
});

export default router;
