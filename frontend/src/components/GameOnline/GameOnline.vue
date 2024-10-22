<template>
  <div class="my-component">
  
	<header>
	  <h1 id="score">Score 0 - 0 </h1>
	  <input type="checkbox" id="volume">
		<img src="/assets/icons/mute.svg" alt="volume mute" id="mute">
		<img src="/assets/icons/unmute.svg" alt="volume unmute" id="unmute">
    <button @click="this.$router.go(-1)" id="goBackButton"></button>
			<img src="/assets/icons/reply.svg" alt="go back" id="goBackIcon" >
	  </input>
	</header>
  
	<div class="waiting-screen" id="loading">
	  <img src="/assets/icons/line-md--loading-twotone-loop.svg" alt="loading">
	</div>
	<div class="waiting-screen" id="waiting-text">
	  <h1>Waiting for players...</h1>
	</div>
  
	<section> 
	  <aside id="countdown-container">
		<h1 id="countdown">3</h1>
	  </aside>
	  <aside id="left-keys">
		<h2 class="keys">W</h2>
		<h2 class="keys">S</h2>
	  </aside>
	  <aside id="right-keys">
		<h2 class="keys">↑</h2>
		<h2 class="keys">↓</h2>
	  </aside>
	</section>
  
	<div ref="canvas"></div>
  
	<div data-testid="joystick-base" id="up-mobile-button" style="border-radius: 100px; height: 100px; width: 100px; background: rgba(255, 255, 255, 0.5); display: flex; justify-content: center; align-items: center; visibility: hidden;">
	  <button style="border-radius: 100px; background: rgba(255, 255, 255, 0.5); cursor: move; height: 66.6667px; width: 66.6667px; border: none; flex-shrink: 0; touch-action: none;"></button>
	</div>
  
	<div data-testid="joystick-base" id="down-mobile-button" style="border-radius: 100px; height: 100px; width: 100px; background: rgba(255, 255, 255, 0.5); display: flex; justify-content: center; align-items: center; visibility: hidden;">
	  <button style="border-radius: 100px; background: rgba(255, 255, 255, 0.5); cursor: move; height: 66.6667px; width: 66.6667px; border: none; flex-shrink: 0; touch-action: none;"></button>
	</div>
  </div>  
</template>
  
<script src="./index.js">
</script>

<style scoped>
.my-component {
	/* background-image: radia
	l-gradient( circle 311px at 8.6% 27.9%,  rgba(62,147,252,0.57) 12.9%, rgba(239,183,192,0.44) 91.2% ); */
  /* background-image: linear-gradient( 184.1deg,  rgba(249,255,182,1) 44.7%, rgba(226,255,172,1) 67.2% ); */
  /* background-image: radial-gradient( circle 918px at 13.1% 25.5%,  rgba(249,107,107,1) 0%, rgba(247,231,172,1) 48.9%, rgba(173,247,172,1) 90% ); */
  /* background-image: radial-gradient( circle 918px at 13.1% 25.5%,  rgba(173,247,172,1)  0%, rgba(247,231,172,1) 48.9%, rgba(249,107,107,1) 90% ); */
  /* background-image: radial-gradient( circle farthest-corner at 10% 20%,  rgba(230,115,1,0.68) 21.4%, rgba(255,78,78,1) 80.3% ); */
  /* background-image: linear-gradient( 109.6deg,  rgba(254,253,205,1) 11.2%, rgba(163,230,255,1) 91.1% ); */
  /* background-image: linear-gradient( 90.5deg,  rgba(152,45,255,1) 0.7%, rgba(90,241,255,1) 51.5%, rgba(65,239,164,1) 100.6% ); */
  /* background-image: radial-gradient( circle farthest-corner at 10% 20%,  rgba(226,240,254,1) 0%, rgba(255,247,228,1) 90% ); */
  background-image: radial-gradient( circle farthest-corner at 10% 20%,  rgba(232,200,72,1) 0%, rgba(204,107,163,1) 100.7% );
  
  background-size: 200% 200%;
  animation: gradientMove 5s infinite alternate;

}
@keyframes gradientMove {
  0% {
    background-position: 0% 0%;
  }
  100% {
    background-position: 100% 100%;
  }
}
body {
  overflow: hidden;
  margin: 0;
  height: 100%;
  place-content: center;
  z-index: 1;
}
body {
  user-select: none;           /* Disallow text selection */
  -webkit-user-select: none;   /* Safari */
  -moz-user-select: none;      /* Firefox */
  -ms-user-select: none;       /* Internet Explorer */
  margin: 0;
  /* height: 100%; */
}
canvas {
  display: block;
  z-index: 100;
}
#score {
  display: flexbox;
  /* justify-content: center; */
  /* align-items: center; */
  margin-top: 6%;
  margin-left: 22%;
  margin-right: 20%;
  position: absolute;
  font-family: monospace;
  font-size: 2.5em;
  visibility: hidden;
  padding: 10px;
}
header {
  /* display: flexbox; */
  justify-content: center;
  align-items: center;
  margin-left: 20%;
  margin-right: 20%;
}
#right-keys {
  position: absolute;
  top: 18%;
  right: 25%;
  padding: 10px;
}
#left-keys {
  position: absolute;
  top: 18%;
  left: 25%;
  padding: 10px;
  /* text-align: center; */
}
.keys {
  font-size: 40px;
  font-family: "SUSE";
  letter-spacing: 1;
  width: 90px;
  height: 90px;
  border: none;
  outline: none;
  background: rgba(255, 255, 255, 0.3);
  border-radius: 20%;
  text-align: center;
  text-align-last: center;
  padding: 10px;
  background-color: seashell;
  justify-content: center;
  align-items: center;
  box-shadow: 5px 5px 10px black, -3px -2px 20px rgba(255, 255, 255, 0.626);
  letter-spacing: 1px;
  visibility: hidden;
}
.keys:hover {
  background-color: #f0f0f0;
  box-shadow: 5px 5px 10px black, -3px -2px 20px rgba(255, 255, 255, 0.626);
}
#countdown {
  font-size: 100px;
  font-family: "SUSE";
  padding: 10px;

  justify-content: center;
  align-items: center;
}
#countdown-container {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  display: flex;
  align-items: center;
  justify-content: center;
  visibility: hidden;
}

#up-mobile-button {
  position: absolute;
  bottom: 10%;
  right: 10%;
}

#down-mobile-button {
  position: absolute;
  bottom: 10%;
  left: 10%;
}

.waiting-screen {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  display: flex;
  align-items: center;
  justify-content: center;
  /* background-color: aqua; */
  /* visibility: hidden; */
 
}

body {
  background-image: radial-gradient( circle 311px at 8.6% 27.9%,  rgba(62,147,252,0.57) 12.9%, rgba(239,183,192,0.44) 91.2% );
  /* background-image: linear-gradient( 184.1deg,  rgba(249,255,182,1) 44.7%, rgba(226,255,172,1) 67.2% ); */
}

#waiting-text {
  animation: move 2s infinite alternate;
  font-family: "SUSE";
  padding: 10px;
  justify-content: center;
  align-items: center;
}

@keyframes move {
  0% {
    transform: translate(-50%, -50%) translateY(0);
  }
  100% {
    transform: translate(-50%, -50%) translateY(-20px);
  }
}

#loading {
  /* font-size: 100px; */
  top: 35%;
  left: 50%;
  font-family: "SUSE";
  padding: 10px;
  justify-content: center;
  align-items: center;
}

#volume {
  position: absolute;
  opacity: 0;
  right: 10%;
  top : 5%;
  /* border: black; */
  cursor: pointer;
  height: 3em;
  width: 3em;
  z-index: 1
}

#mute {
  position: absolute;
  display: none;
  z-index: 0;
  height: 2em;
  width: 2em;
  right: 5%;
  top : 5%;
}

#unmute {
  position: absolute;
  z-index: 0;
  height: 2em;
  width: 2em;
  right: 5%;
  top : 5%;
}

#goBackIcon {
	position: absolute;
  z-index: 0;
  height: 2em;
  width: 2em;
  left: 5%;
  top : 5%;
/* transform: scaleX(-1); */
} 

#goBackButton {
  position: absolute;
  opacity: 0;
  left: 5%;
  top : 5%;
  /* border: black; */
  cursor: pointer;
  height: 3em;
  width: 3em;
  z-index: 1
}


#volume:checked ~ #mute {
  display: block;
}

#volume:checked ~ #unmute {
  display: none;
}


/* @media screen and (max-width: 1000px) and (orientation: landscape) {
  #score {
    font-size: 1.5em;
  }

  .keys {
    font-size: 25px;
    width: 60px;
    height: 60px;
  }

  #up-mobile-button, #down-mobile-button {
    bottom: 5%;
    width: 40px;
    height: 40px;
  }

  #volume, #mute, #unmute {
    height: 1.5em;
    width: 1.5em;
  }
} */

/* @media screen and (max-width: 600px) and (orientation: portrait) {
  #score {
    margin-top: 10%;
    margin-left: 10%;
    margin-right: 10%;
    font-size: 1.8em;
  }

  .keys {
    font-size: 30px;
    width: 70px;
    height: 70px;
  }

  #up-mobile-button, #down-mobile-button {
    bottom: 5%;
    width: 50px;
    height: 50px;
  }

  #volume, #mute, #unmute {
    height: 2em;
    width: 2em;
  }
} */

@media screen and (max-width: 600px ) {
  #score {
    margin-top: 10%;
    margin-left: 10%;
    margin-right: 10%;
    align-items: center;
    font-size: 1.8em;
  }

  .keys {
    font-size: 30px;
    width: 70px;
    height: 70px;     display: noneu  }n-mobile-button {
    bottom: 5%;
    width: 50px;
    height: 50px;
  } 
}
</style>
  