!function(){var s="header-common";document.getElementsByClassName(s)[0].classList.add("clone");let e=document.querySelector(".header4LogoChange");window.onscroll=function(){var t=document.body.classList;if(window.pageYOffset>150?(document.getElementsByClassName(s+" clone")[0].classList.add("initialized"),t.add("sticky")):t.remove("sticky"),e&&e?.classList.contains("clone")){let o=document.querySelector("html"),a=e.querySelector(".logo"),c=a.getAttribute("src"),l="../assets/images/logos/logo-4-w.png";t.contains("sticky")&&o.classList.contains("dark")&&c!==l?a.setAttribute("src",l):t.contains("sticky")||a.setAttribute("src","../assets/images/logos/logo-4.png")}}}();