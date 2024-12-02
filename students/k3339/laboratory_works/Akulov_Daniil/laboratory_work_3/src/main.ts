import * as process from "node:process";
import {NestFactory} from "@nestjs/core";
import {AppModule} from "./app.module";
import {DocumentBuilder, SwaggerModule} from "@nestjs/swagger";
import {BadRequestException, ValidationPipe} from "@nestjs/common";

async function start(){
    const PORT = process.env.PORT || 5000
    const app = await NestFactory.create(AppModule)

    const config = new DocumentBuilder()
        .setTitle("Sound Sphere API")
        .setVersion('1.0.0')
        .setDescription('Source code: https://github.com/pheroom/sound-sphere-backend')
        .build()
    const document = SwaggerModule.createDocument(app, config);
    SwaggerModule.setup('/api/docs', app, document);

    // app.setGlobalPrefix('api')
    app.useGlobalPipes(new ValidationPipe({
        exceptionFactory: (errors) => {
            const result = errors.map((error) => ({
                property: error.property,
                message: error.constraints[Object.keys(error.constraints)[0]],
            }));
            return new BadRequestException(result);
        },
        stopAtFirstError: true,
    }));

    await app.listen(PORT, () => console.log(`Listening on ${PORT}`))
}

start()