(function (a) {
    function t(t) {
        for (var r, o, s = t[0], d = t[1], c = t[2], l = 0, p = []; l < s.length; l++) o = s[l], Object.prototype.hasOwnProperty.call(i, o) && i[o] && p.push(i[o][0]), i[o] = 0;
        for (r in d) Object.prototype.hasOwnProperty.call(d, r) && (a[r] = d[r]);
        u && u(t);
        while (p.length) p.shift()();
        return n.push.apply(n, c || []), e()
    }

    function e() {
        for (var a, t = 0; t < n.length; t++) {
            for (var e = n[t], r = !0, o = 1; o < e.length; o++) {
                var s = e[o];
                0 !== i[s] && (r = !1)
            }
            r && (n.splice(t--, 1), a = d(d.s = e[0]))
        }
        return a
    }
    var r = {},
        o = {
            app: 0
        },
        i = {
            app: 0
        },
        n = [];

    function s(a) {
        return d.p + "js/" + ({
            almocos: "almocos",
            "atividades~departamentoatividades~inscricao~minhasatividades~transportes": "atividades~departamentoatividades~inscricao~minhasatividades~transportes",
            atividades: "atividades",
            minhasatividades: "minhasatividades",
            "colaboradores~departamentoatividades~inscricao~proporatividade~tarefas~transportes": "colaboradores~departamentoatividades~inscricao~proporatividade~tarefas~transportes",
            departamentoatividades: "departamentoatividades",
            inscricao: "inscricao",
            transportes: "transportes",
            colaboradores: "colaboradores",
            proporatividade: "proporatividade",
            tarefas: "tarefas",
            configuracao: "configuracao",
            inscricoes: "inscricoes"
        } [a] || a) + "." + {
            almocos: "09b06c28",
            "atividades~departamentoatividades~inscricao~minhasatividades~transportes": "7db513bd",
            atividades: "f0c6cdde",
            minhasatividades: "ecc268e6",
            "chunk-1823af82": "4d78cc6e",
            "colaboradores~departamentoatividades~inscricao~proporatividade~tarefas~transportes": "38d827a4",
            departamentoatividades: "8a11ada1",
            inscricao: "689ad7a7",
            transportes: "c3d4bfc2",
            colaboradores: "03a794e1",
            proporatividade: "46ad7021",
            tarefas: "268f7ccd",
            configuracao: "dddc62e3",
            inscricoes: "a76322c7"
        } [a] + ".js"
    }

    function d(t) {
        if (r[t]) return r[t].exports;
        var e = r[t] = {
            i: t,
            l: !1,
            exports: {}
        };
        return a[t].call(e.exports, e, e.exports, d), e.l = !0, e.exports
    }
    d.e = function (a) {
        var t = [],
            e = {
                atividades: 1,
                minhasatividades: 1,
                departamentoatividades: 1,
                inscricao: 1,
                transportes: 1,
                colaboradores: 1,
                proporatividade: 1,
                tarefas: 1
            };
        o[a] ? t.push(o[a]) : 0 !== o[a] && e[a] && t.push(o[a] = new Promise((function (t, e) {
            for (var r = "css/" + ({
                    almocos: "almocos",
                    "atividades~departamentoatividades~inscricao~minhasatividades~transportes": "atividades~departamentoatividades~inscricao~minhasatividades~transportes",
                    atividades: "atividades",
                    minhasatividades: "minhasatividades",
                    "colaboradores~departamentoatividades~inscricao~proporatividade~tarefas~transportes": "colaboradores~departamentoatividades~inscricao~proporatividade~tarefas~transportes",
                    departamentoatividades: "departamentoatividades",
                    inscricao: "inscricao",
                    transportes: "transportes",
                    colaboradores: "colaboradores",
                    proporatividade: "proporatividade",
                    tarefas: "tarefas",
                    configuracao: "configuracao",
                    inscricoes: "inscricoes"
                } [a] || a) + "." + {
                    almocos: "31d6cfe0",
                    "atividades~departamentoatividades~inscricao~minhasatividades~transportes": "31d6cfe0",
                    atividades: "320507fe",
                    minhasatividades: "320507fe",
                    "chunk-1823af82": "31d6cfe0",
                    "colaboradores~departamentoatividades~inscricao~proporatividade~tarefas~transportes": "31d6cfe0",
                    departamentoatividades: "11740b86",
                    inscricao: "1e7f0088",
                    transportes: "9d1670f9",
                    colaboradores: "2c4c9dc5",
                    proporatividade: "dbff9dac",
                    tarefas: "91a2a446",
                    configuracao: "31d6cfe0",
                    inscricoes: "31d6cfe0"
                } [a] + ".css", i = d.p + r, n = document.getElementsByTagName("link"), s = 0; s < n.length; s++) {
                var c = n[s],
                    l = c.getAttribute("data-href") || c.getAttribute("href");
                if ("stylesheet" === c.rel && (l === r || l === i)) return t()
            }
            var p = document.getElementsByTagName("style");
            for (s = 0; s < p.length; s++) {
                c = p[s], l = c.getAttribute("data-href");
                if (l === r || l === i) return t()
            }
            var u = document.createElement("link");
            u.rel = "stylesheet", u.type = "text/css", u.onload = t, u.onerror = function (t) {
                var r = t && t.target && t.target.src || i,
                    n = new Error("Loading CSS chunk " + a + " failed.\n(" + r + ")");
                n.code = "CSS_CHUNK_LOAD_FAILED", n.request = r, delete o[a], u.parentNode.removeChild(u), e(n)
            }, u.href = i;
            var m = document.getElementsByTagName("head")[0];
            m.appendChild(u)
        })).then((function () {
            o[a] = 0
        })));
        var r = i[a];
        if (0 !== r)
            if (r) t.push(r[2]);
            else {
                var n = new Promise((function (t, e) {
                    r = i[a] = [t, e]
                }));
                t.push(r[2] = n);
                var c, l = document.createElement("script");
                l.charset = "utf-8", l.timeout = 120, d.nc && l.setAttribute("nonce", d.nc), l.src = s(a);
                var p = new Error;
                c = function (t) {
                    l.onerror = l.onload = null, clearTimeout(u);
                    var e = i[a];
                    if (0 !== e) {
                        if (e) {
                            var r = t && ("load" === t.type ? "missing" : t.type),
                                o = t && t.target && t.target.src;
                            p.message = "Loading chunk " + a + " failed.\n(" + r + ": " + o + ")", p.name = "ChunkLoadError", p.type = r, p.request = o, e[1](p)
                        }
                        i[a] = void 0
                    }
                };
                var u = setTimeout((function () {
                    c({
                        type: "timeout",
                        target: l
                    })
                }), 12e4);
                l.onerror = l.onload = c, document.head.appendChild(l)
            } return Promise.all(t)
    }, d.m = a, d.c = r, d.d = function (a, t, e) {
        d.o(a, t) || Object.defineProperty(a, t, {
            enumerable: !0,
            get: e
        })
    }, d.r = function (a) {
        "undefined" !== typeof Symbol && Symbol.toStringTag && Object.defineProperty(a, Symbol.toStringTag, {
            value: "Module"
        }), Object.defineProperty(a, "__esModule", {
            value: !0
        })
    }, d.t = function (a, t) {
        if (1 & t && (a = d(a)), 8 & t) return a;
        if (4 & t && "object" === typeof a && a && a.__esModule) return a;
        var e = Object.create(null);
        if (d.r(e), Object.defineProperty(e, "default", {
                enumerable: !0,
                value: a
            }), 2 & t && "string" != typeof a)
            for (var r in a) d.d(e, r, function (t) {
                return a[t]
            }.bind(null, r));
        return e
    }, d.n = function (a) {
        var t = a && a.__esModule ? function () {
            return a["default"]
        } : function () {
            return a
        };
        return d.d(t, "a", t), t
    }, d.o = function (a, t) {
        return Object.prototype.hasOwnProperty.call(a, t)
    }, d.p = "/", d.oe = function (a) {
        throw console.error(a), a
    };
    var c = window["webpackJsonp"] = window["webpackJsonp"] || [],
        l = c.push.bind(c);
    c.push = t, c = c.slice();
    for (var p = 0; p < c.length; p++) t(c[p]);
    var u = l;
    n.push([0, "chunk-vendors"]), e()
})({
    0: function (a, t, e) {
        a.exports = e("56d7")
    },
    "0ba8": function (a, t, e) {
        "use strict";
        var r = e("df25"),
            o = e.n(r);
        o.a
    },
    "1df7": function (a, t, e) {
        "use strict";
        var r = e("1e23"),
            o = e.n(r);
        o.a
    },
    "1e23": function (a, t, e) {},
    "56d7": function (a, t, e) {
        "use strict";
        e.r(t);
        e("e260"), e("e6cf"), e("cca6"), e("a79d");
        var r = e("2b0e"),
            o = function () {
                var a = this,
                    t = a.$createElement,
                    e = a._self._c || t;
                return e("div", {
                    attrs: {
                        id: "app"
                    }
                }, [e("NavBar"), a._m(0), e("div", {
                    attrs: {
                        id: "page-content"
                    }
                }, [e("div", {
                    staticClass: "card"
                }, [e("div", {
                    staticClass: "card-content"
                }, [e("router-view")], 1)])]), a._m(1)], 1)
            },
            i = [function () {
                var a = this,
                    t = a.$createElement,
                    e = a._self._c || t;
                return e("div", {
                    staticClass: "hero is-primary is-bold",
                    attrs: {
                        id: "top-hero"
                    }
                }, [e("div", {
                    staticClass: "hero-body",
                    attrs: {
                        id: "top-hero-body"
                    }
                })])
            }, function () {
                var a = this,
                    t = a.$createElement,
                    e = a._self._c || t;
                return e("footer", {
                    staticClass: "footer"
                }, [e("div", {
                    staticStyle: {
                        float: "left"
                    }
                }, [a._v(" (c) 2020 ")]), e("div", {
                    staticStyle: {
                        float: "right"
                    }
                }, [a._v(" Designed by Grupo 9 ")]), e("div", {
                    staticStyle: {
                        margin: "auto",
                        width: "max-content"
                    }
                }, [a._v(" Dia Aberto ")])])
            }],
            n = function () {
                var a = this,
                    t = a.$createElement,
                    r = a._self._c || t;
                return r("b-navbar", [r("template", {
                    slot: "brand"
                }, [r("b-navbar-item", {
                    staticClass: "logo",
                    attrs: {
                        to: {
                            name: "inicio"
                        },
                        tag: "router-link"
                    }
                }, [r("img", {
                    attrs: {
                        alt: "Dia Aberto",
                        src: e("db6c")
                    }
                })])], 1), r("template", {
                    slot: "start"
                }, [a._l(a.separadores[a.$store.state.utilizador], (function (t, e) {
                    return [r("b-navbar-item", {
                        key: e,
                        staticClass: "is-tab router-link",
                        attrs: {
                            to: {
                                name: t.nome
                            },
                            tag: "router-link"
                        }
                    }, [a._v(" " + a._s(t.descricao) + " ")])]
                }))], 2), r("template", {
                    slot: "end"
                }, [r("b-navbar-item", {
                    attrs: {
                        tag: "div"
                    }
                }, [r("b-dropdown", {
                    attrs: {
                        position: "is-bottom-left",
                        "aria-role": "menu"
                    },
                    model: {
                        value: a.navigation,
                        callback: function (t) {
                            a.navigation = t
                        },
                        expression: "navigation"
                    }
                }, [r("span", {
                    attrs: {
                        slot: "trigger",
                        role: "button"
                    },
                    slot: "trigger"
                }, [r("b-button", {
                    staticClass: "has-badge-rounded has-badge-warning",
                    staticStyle: {
                        "margin-right": "0.9rem"
                    },
                    attrs: {
                        type: "is-text",
                        "data-badge": a.$store.state.notificacoes.length
                    }
                }, [r("b-icon", {
                    attrs: {
                        icon: "bell"
                    }
                })], 1)], 1), r("b-dropdown-item", {
                    attrs: {
                        custom: "",
                        "aria-role": "menuitem"
                    }
                }, [r("strong", [a._v("Notificações")])]), r("hr", {
                    staticClass: "dropdown-divider"
                }), a._l(a.$store.state.notificacoes, (function (t, e) {
                    return r("div", {
                        key: e
                    }, [r("b-dropdown-item", {
                        attrs: {
                            "has-link": "",
                            "aria-role": "menuitem"
                        }
                    }, [r("a", {
                        staticStyle: {
                            width: "18rem",
                            "white-space": "initial"
                        }
                    }, [a._v(" " + a._s(t) + " ")])]), r("b-dropdown-item", {
                        attrs: {
                            separator: ""
                        }
                    })], 1)
                })), 0 === a.$store.state.notificacoes.length ? r("div", [r("b-dropdown-item", {
                    attrs: {
                        custom: ""
                    }
                }, [r("div", {
                    staticClass: "has-text-grey"
                }, [a._v(" Não tem novas notificações! ")])]), r("b-dropdown-item", {
                    attrs: {
                        separator: ""
                    }
                })], 1) : a._e(), r("b-dropdown-item", [r("u", [a._v("Ver todas as notificações")])])], 2), r("b-dropdown", {
                    attrs: {
                        "aria-role": "list",
                        position: "is-bottom-left"
                    }
                }, [r("b-button", {
                    staticStyle: {
                        "margin-right": "0.9rem"
                    },
                    attrs: {
                        slot: "trigger",
                        type: "is-text"
                    },
                    slot: "trigger"
                }, [r("b-icon", {
                    attrs: {
                        icon: "account-circle"
                    }
                })], 1), r("b-dropdown-item", {
                    attrs: {
                        "aria-role": "listitem",
                        disabled: ""
                    }
                }, [a._v("Participante Individual")]), r("b-dropdown-item", {
                    attrs: {
                        "aria-role": "listitem"
                    },
                    on: {
                        click: function (t) {
                            return a.mudarUtilizador("professorSecundario")
                        }
                    }
                }, [a._v("Professor Secundário")]), r("b-dropdown-item", {
                    attrs: {
                        "aria-role": "listitem",
                        disabled: ""
                    }
                }, [a._v("Colaborador")]), r("b-dropdown-item", {
                    attrs: {
                        "aria-role": "listitem"
                    },
                    on: {
                        click: function (t) {
                            return a.mudarUtilizador("professorUniversitario")
                        }
                    }
                }, [a._v("Professor Universitário")]), r("b-dropdown-item", {
                    attrs: {
                        "aria-role": "listitem"
                    },
                    on: {
                        click: function (t) {
                            return a.mudarUtilizador("coordenador")
                        }
                    }
                }, [a._v("Coordenador")]), r("b-dropdown-item", {
                    attrs: {
                        "aria-role": "listitem"
                    },
                    on: {
                        click: function (t) {
                            return a.mudarUtilizador("administrador")
                        }
                    }
                }, [a._v("Administrador")])], 1), r("b-button", {
                    attrs: {
                        "icon-left": "logout-variant"
                    }
                }, [a._v(" Sair ")])], 1)], 1)], 2)
            },
            s = [],
            d = {
                name: "NavBar",
                data: function () {
                    return {
                        separadores: {
                            administrador: [{
                                nome: "atividades",
                                descricao: "Atividades"
                            }, {
                                nome: "inscricoes",
                                descricao: "Inscrições"
                            }, {
                                nome: "transportes",
                                descricao: "Transportes"
                            }, {
                                nome: "almocos",
                                descricao: "Almoços"
                            }, {
                                nome: "configuracao do dia aberto",
                                descricao: "Configuração do Dia Aberto"
                            }],
                            professorSecundario: [{
                                nome: "inscricao",
                                descricao: "Minha Inscrição"
                            }],
                            professorUniversitario: [{
                                nome: "minhas atividades",
                                descricao: "Minhas Atividades"
                            }],
                            coordenador: [{
                                nome: "atividades do departamento",
                                descricao: "Atividades do Departamento"
                            }, {
                                nome: "inscricoes",
                                descricao: "Inscrições"
                            }, {
                                nome: "colaboradores",
                                descricao: "Colaboradores"
                            }, {
                                nome: "tarefas",
                                descricao: "Tarefas"
                            }]
                        }
                    }
                },
                methods: {
                    mudarUtilizador: function (a) {
                        this.$store.commit("mudarUtilizador", a)
                    }
                }
            },
            c = d,
            l = (e("0ba8"), e("2877")),
            p = Object(l["a"])(c, n, s, !1, null, "a67fe1ba", null),
            u = p.exports,
            m = {
                components: {
                    NavBar: u
                }
            },
            f = m,
            v = (e("1df7"), Object(l["a"])(f, o, i, !1, null, "8716d23a", null)),
            b = v.exports,
            h = (e("d3b7"), e("8c4f"));
        r["a"].use(h["a"]);
        var g = [{
                path: "/",
                name: "inicio",
                component: function () {
                    return e.e("chunk-1823af82").then(e.bind(null, "b53f"))
                }
            }, {
                path: "/atividades",
                name: "atividades",
                component: function () {
                    return Promise.all([e.e("atividades~departamentoatividades~inscricao~minhasatividades~transportes"), e.e("atividades")]).then(e.bind(null, "3438"))
                }
            }, {
                path: "/inscricoes",
                name: "inscricoes",
                component: function () {
                    return e.e("inscricoes").then(e.bind(null, "4982"))
                }
            }, {
                path: "/transportes",
                name: "transportes",
                component: function () {
                    return Promise.all([e.e("colaboradores~departamentoatividades~inscricao~proporatividade~tarefas~transportes"), e.e("atividades~departamentoatividades~inscricao~minhasatividades~transportes"), e.e("transportes")]).then(e.bind(null, "5f4f"))
                }
            }, {
                path: "/adicionartransporte",
                name: "adicionar transporte",
                component: function () {
                    return Promise.all([e.e("colaboradores~departamentoatividades~inscricao~proporatividade~tarefas~transportes"), e.e("atividades~departamentoatividades~inscricao~minhasatividades~transportes"), e.e("transportes")]).then(e.bind(null, "e966"))
                }
            }, {
                path: "/almocos",
                name: "almocos",
                component: function () {
                    return e.e("almocos").then(e.bind(null, "3026"))
                }
            }, {
                path: "/configuracao",
                name: "configuracao do dia aberto",
                component: function () {
                    return e.e("configuracao").then(e.bind(null, "07c4"))
                }
            }, {
                path: "/inscricao",
                name: "inscricao",
                component: function () {
                    return Promise.all([e.e("colaboradores~departamentoatividades~inscricao~proporatividade~tarefas~transportes"), e.e("atividades~departamentoatividades~inscricao~minhasatividades~transportes"), e.e("inscricao")]).then(e.bind(null, "cdcc"))
                }
            }, {
                path: "/minhasatividades",
                name: "minhas atividades",
                component: function () {
                    return Promise.all([e.e("atividades~departamentoatividades~inscricao~minhasatividades~transportes"), e.e("minhasatividades")]).then(e.bind(null, "337d"))
                }
            }, {
                path: "/proporatividade",
                name: "propor atividade",
                component: function () {
                    return Promise.all([e.e("colaboradores~departamentoatividades~inscricao~proporatividade~tarefas~transportes"), e.e("proporatividade")]).then(e.bind(null, "f999"))
                }
            }, {
                path: "/departamentoatividades",
                name: "atividades do departamento",
                component: function () {
                    return Promise.all([e.e("colaboradores~departamentoatividades~inscricao~proporatividade~tarefas~transportes"), e.e("atividades~departamentoatividades~inscricao~minhasatividades~transportes"), e.e("departamentoatividades")]).then(e.bind(null, "f8de"))
                }
            }, {
                path: "/colaboradores",
                name: "colaboradores",
                component: function () {
                    return Promise.all([e.e("colaboradores~departamentoatividades~inscricao~proporatividade~tarefas~transportes"), e.e("colaboradores")]).then(e.bind(null, "d641"))
                }
            }, {
                path: "/tarefas",
                name: "tarefas",
                component: function () {
                    return Promise.all([e.e("colaboradores~departamentoatividades~inscricao~proporatividade~tarefas~transportes"), e.e("tarefas")]).then(e.bind(null, "25f9"))
                }
            }, {
                path: "/adicionartarefa",
                name: "adicionar tarefa",
                component: function () {
                    return Promise.all([e.e("colaboradores~departamentoatividades~inscricao~proporatividade~tarefas~transportes"), e.e("tarefas")]).then(e.bind(null, "7592"))
                }
            }],
            y = new h["a"]({
                mode: "history",
                base: "/",
                routes: g
            }),
            w = y,
            _ = e("2f62");
        r["a"].use(_["a"]);
        var O = new _["a"].Store({
                state: {
                    utilizador: "administrador",
                    estadoSubmissao: {
                        A: {
                            descricao: "Aceite",
                            cor: "is-success"
                        },
                        P: {
                            descricao: "Pendente",
                            cor: "is-warning"
                        },
                        R: {
                            descricao: "Rejeitada",
                            cor: "is-danger"
                        }
                    },
                    notificacoes: [],
                    inscritos: [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    tarefa: !1
                },
                mutations: {
                    mudarUtilizador: function (a, t) {
                        a.utilizador = t, a.notificacoes = [], a.tarefa = !1, a.inscritos = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], w.push({
                            name: "inicio"
                        })
                    },
                    adicionarNotificacao: function (a, t) {
                        a.notificacoes.push(t)
                    },
                    mudarInscritos: function (a, t, e) {
                        a.inscritos[t] = e
                    },
                    carregarTarefa: function (a) {
                        a.tarefa = !0
                    }
                },
                actions: {},
                modules: {}
            }),
            P = (e("a4d3"), e("4de4"), e("4160"), e("e439"), e("dbb4"), e("b64b"), e("159b"), e("96cf"), e("fc11")),
            k = e("522d"),
            j = e("efe7");

        function C(a, t) {
            var e = Object.keys(a);
            if (Object.getOwnPropertySymbols) {
                var r = Object.getOwnPropertySymbols(a);
                t && (r = r.filter((function (t) {
                    return Object.getOwnPropertyDescriptor(a, t).enumerable
                }))), e.push.apply(e, r)
            }
            return e
        }

        function S(a) {
            for (var t = 1; t < arguments.length; t++) {
                var e = null != arguments[t] ? arguments[t] : {};
                t % 2 ? C(Object(e), !0).forEach((function (t) {
                    Object(P["a"])(a, t, e[t])
                })) : Object.getOwnPropertyDescriptors ? Object.defineProperties(a, Object.getOwnPropertyDescriptors(e)) : C(Object(e)).forEach((function (t) {
                    Object.defineProperty(a, t, Object.getOwnPropertyDescriptor(e, t))
                }))
            }
            return a
        }
        r["a"].use(k["a"]);
        var x = "apollo-token",
            E = "http://localhost:8000/graphql",
            A = {
                httpEndpoint: E,
                wsEndpoint: null,
                tokenName: x,
                persisting: !1,
                websocketsOnly: !1,
                ssr: !1
            };

        function N() {
            var a = arguments.length > 0 && void 0 !== arguments[0] ? arguments[0] : {},
                t = Object(j["createApolloClient"])(S({}, A, {}, a)),
                e = t.apolloClient,
                r = t.wsClient;
            e.wsClient = r;
            var o = new k["a"]({
                defaultClient: e,
                defaultOptions: {
                    $query: {
                        fetchPolicy: "cache-and-network"
                    }
                },
                errorHandler: function (a) {
                    console.log("%cError", "background: red; color: white; padding: 2px 4px; border-radius: 3px; font-weight: bold;", a.message)
                }
            });
            return o
        }
        var D = e("289d");
        r["a"].use(D["a"]);
        e("5788");
        var T = e("f13c"),
            U = e.n(T);
        r["a"].use(U.a, {
            duration: 300
        });
        e("5363");
        r["a"].config.productionTip = !1, new r["a"]({
            router: w,
            store: O,
            apolloProvider: N(),
            render: function (a) {
                return a(b)
            }
        }).$mount("#app")
    },
    5788: function (a, t, e) {},
    db6c: function (a, t, e) {
        a.exports = e.p + "img/logo-navbar.1a946f02.png"
    },
    df25: function (a, t, e) {}
});
//# sourceMappingURL=app.841e44b5.js.map