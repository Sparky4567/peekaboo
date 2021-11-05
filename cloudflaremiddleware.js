async function alterHeaders(req) {
	//Request url
	const url = new URL(req.request.url);
	let FULL_URL = `https://${url.hostname}${url.pathname}`;
	if (FULL_URL.includes(".html")) {
		FULL_URL = FULL_URL.replace(".html", "");
	}

	//Auth headers
	const AUTH_HEADERS = {
		Authorization: "Basic token",
		"Check-Url": FULL_URL,
	};

	//Peekaboo url

	const PEEKABOO = "http://ipaddress:8000/get";

	//BOT array
	const BOT_AGENTS = [
		"googlebot",
		"yahoo! slurp",
		"bingbot",
		"yandex",
		"baiduspider",
		"facebookexternalhit",
		"twitterbot",
		"rogerbot",
		"linkedinbot",
		"embedly",
		"quora link preview",
		"showyoubot",
		"outbrain",
		"pinterest/0.",
		"developers.google.com/+/web/snippet",
		"slackbot",
		"vkshare",
		"w3c_validator",
		"redditbot",
		"applebot",
		"whatsapp",
		"flipboard",
		"tumblr",
		"bitlybot",
		"skypeuripreview",
		"nuzzel",
		"discordbot",
		"google page speed",
		"qwantify",
		"pinterestbot",
		"bitrix link preview",
		"xing-contenttabreceiver",
		"chrome-lighthouse",
		"telegrambot",
	];

	//Checks if User-Agent contains values from the bot array
	function containsOneOfThem(array, element) {
		return array.includes(element);
	}

	//Gets headers
	let requestHeaders = req.request.headers;
	//Gets user agent
	let requestUserAgent = requestHeaders.get("User-Agent");
	requestUserAgent = String(requestUserAgent).toLowerCase();

	//Gets peekaboo User-Agent

	let peekabooprerender = requestHeaders.get("Peekaboo-Prerender");
	//Not peekaboo, but one of the bots? Oh, we got you now.
	if (
		peekabooprerender === null &&
		containsOneOfThem(BOT_AGENTS, requestUserAgent) === true
	) {
		//Forming new headers
		let res = await fetch(PEEKABOO, { method: "GET", headers: AUTH_HEADERS });
		let newHeaders = new Headers(res.headers);
		newHeaders.set("Content-Type", "text/html;charset=UTF-8");
		newHeaders.set("Server", "ArtefaktasServer");
		newHeaders.set("X-Frame-Options", "DENY");
		newHeaders.set("Content-Security-Policy", "upgrade-insecure-requests;");
		newHeaders.set(
			"Strict-Transport-Security",
			"max-age=63072000; includeSubDomains; preload"
		);
		newHeaders.set("X-Xss-Protection", "1; mode=block");
		newHeaders.set("X-Content-Type-Options", "nosniff");
		newHeaders.set("Referrer-Policy", "strict-origin-when-cross-origin");
		newHeaders.set("Host", "www.artefaktas.eu");
		newHeaders.set("Cache-Control", "max-age=14400, s-maxage=14400");
		newHeaders.set("Permissions-Policy", "geolocation=(), microphone=()");
		newHeaders.set("Peekaboo-Working", "yes");

		let d = await res.json();
		if (d.status !== false) {
			///Muhahahaha ! No CSS and JavaScript for you.
			return new Response(d.status, {
				headers: newHeaders,
			});
		} else {
			let response = await fetch(req.request);
			let newHeaders = new Headers(response.headers);
			newHeaders.set("Content-Type", "text/html;charset=UTF-8");
			newHeaders.set("Server", "ArtefaktasServer");
			newHeaders.set("X-Frame-Options", "DENY");
			newHeaders.set("Content-Security-Policy", "upgrade-insecure-requests;");
			newHeaders.set(
				"Strict-Transport-Security",
				"max-age=63072000; includeSubDomains; preload"
			);
			newHeaders.set("X-Xss-Protection", "1; mode=block");
			newHeaders.set("X-Content-Type-Options", "nosniff");
			newHeaders.set("Referrer-Policy", "strict-origin-when-cross-origin");
			newHeaders.set("Host", "www.artefaktas.eu");
			newHeaders.set("Cache-Control", "max-age=14400, s-maxage=14400");
			newHeaders.set("Permissions-Policy", "geolocation=(), microphone=()");
			newHeaders.set("Peekaboo-Working", "yes");
			return new Response(response.body, {
				headers: newHeaders,
			});
		}
	} else {
		//Making new request by url to the cache
		let response = await fetch(req.request);

		//Altering headers
		let newHeaders = new Headers(response.headers);
		newHeaders.set("Server", "ArtefaktasServer");
		newHeaders.set("X-Frame-Options", "DENY");
		newHeaders.set("Content-Security-Policy", "upgrade-insecure-requests;");
		newHeaders.set(
			"Strict-Transport-Security",
			"max-age=63072000; includeSubDomains; preload"
		);
		newHeaders.set("X-Xss-Protection", "1; mode=block");
		newHeaders.set("X-Content-Type-Options", "nosniff");
		newHeaders.set("Referrer-Policy", "strict-origin-when-cross-origin");
		newHeaders.set("Host", "www.artefaktas.eu");
		newHeaders.set("Cache-Control", "max-age=14400, s-maxage=14400");
		newHeaders.set("Permissions-Policy", "geolocation=(), microphone=()");

		let modified = new Response(response.body, {
			status: response.status,
			statusText: response.statusText,
			headers: newHeaders,
		});

		return modified;
		//Yes? Oh ... Let us return the response then.
	}
}

addEventListener("fetch", (event) => {
	event.respondWith(alterHeaders(event));
});
